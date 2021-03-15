from numpy.lib.function_base import append
import tensorflow.compat.v1 as tf
import ctc_utils
import cv2
import numpy as np
import sys
from midi.player import *
import simpleaudio as sa
import re

note_r = re.compile("(note|gracenote)-([A-G][b|#]?[0-9])_(.*)$")
other_r = re.compile("(clef|keySignature|timeSignature|rest|multirest)-(.*)$")

# Automatic brightness and contrast optimization with optional histogram clipping


def automatic_brightness_and_contrast(image, clip_hist_percent=1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index - 1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size - 1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)


def split_score(file_name, tick):
    img = cv2.imread(file_name)

    img, alpha, beta = automatic_brightness_and_contrast(img)
    print(f"alpha:{alpha} beta{beta}\n")

    # define border color
    lower = (0, 80, 110)
    upper = (0, 120, 150)

    # threshold on border color
    mask = cv2.inRange(img, lower, upper)

    # dilate threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # recolor border to white
    img[mask == 255] = (255, 255, 255)

    # convert img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # otsu threshold
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

    # apply morphology open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 17))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    morph = 255 - morph

    # find contours and bounding boxes
    bboxes = []
    contours = cv2.findContours(
        morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    max_weight = 0
    for cntr in contours:
        x, y, w, h = cv2.boundingRect(cntr)
        if w > max_weight:
            max_weight = w
        bboxes.append((x, y, w, h))

    # sort bboxes on y coordinate
    def sort_key(elem):
        return elem[1]

    bboxes.sort(key=sort_key)

    def include_line(line_count, tick):
        return tick == 0 or (tick == 1 and line_count % 2 == 1) or (tick > 1 and line_count % tick == 0)

    lines = []
    line_count = 0
    for bbox in bboxes:
        if abs(bbox[2] - max_weight) < (max_weight / 4):

            if include_line(line_count, tick):
                x = bbox[0]
                y = bbox[1]
                w = bbox[2]
                h = bbox[3]
                print(f"{bbox}\n")
                sample = img[y:y+h, x:x+w]
                lines.append(sample)

            line_count += 1

    return lines


def read_vocab(vocab_semantic):
    # Read the dictionary
    dict_file = open(vocab_semantic, 'r')
    dict_list = dict_file.read().splitlines()
    int2word = dict()
    for word in dict_list:
        word_idx = len(int2word)
        int2word[word_idx] = word
    dict_file.close()

    return int2word


def parse_description(description):
    if description == "barline":
        return ("barline", "", "")

    result = note_r.findall(description)
    if len(result) == 1:
        return result[0]

    result = other_r.findall(description)
    if len(result) == 1:
        return result[0] + ("", )

    return (f"unknown", description, "")


def main(ms_file_name, line_freq, ouptut_file):
    tf.reset_default_graph()
    sess = tf.InteractiveSession()

    # load vocabulary
    int2word = read_vocab("models/vocabulary_semantic.txt")

    # Restore weights
    model = "models/semantic_model.meta"
    saver = tf.train.import_meta_graph(model)
    saver.restore(sess, model[:-5])

    graph = tf.get_default_graph()

    model_input = graph.get_tensor_by_name("model_input:0")
    seq_len = graph.get_tensor_by_name("seq_lengths:0")
    rnn_keep_prob = graph.get_tensor_by_name("keep_prob:0")
    height_tensor = graph.get_tensor_by_name("input_height:0")
    width_reduction_tensor = graph.get_tensor_by_name("width_reduction:0")
    logits = tf.get_collection("logits")[0]

    # Constants that are saved inside the model itself
    WIDTH_REDUCTION, HEIGHT = sess.run([width_reduction_tensor, height_tensor])

    decoded, _ = tf.nn.ctc_greedy_decoder(logits, seq_len)

    # split the music score into lines
    print(f"Process {ms_file_name}\n")
    lines = split_score(ms_file_name, line_freq)

    output = open(ouptut_file, "w")
    # process save file
    for idx, line in enumerate(lines):
        # write the file to sample directory for sampling
        print(f"./samples/sample{idx}.png\n")
        cv2.imwrite(f"./samples/sample{idx}.png", line)

        gray = cv2.cvtColor(line, cv2.COLOR_BGR2GRAY)
        image = ctc_utils.resize(gray, HEIGHT)
        image = ctc_utils.normalize(image)
        image = np.asarray(image).reshape(1, image.shape[0], -1, 1)

        seq_lengths = [image.shape[2] / WIDTH_REDUCTION]

        prediction = sess.run(decoded,
                              feed_dict={
                                  model_input: image,
                                  seq_len: seq_lengths,
                                  rnn_keep_prob: 1.0,
                              })

        str_predictions = ctc_utils.sparse_tensor_to_strs(prediction)

        for w in str_predictions[0]:
            description = int2word[w]
            notation, v1, v2 = parse_description(description)
            if v1 != "tie":
                if notation == "barline":
                    output.write("### ----------------\n")
                elif notation == "note" or notation == "gracenote":
                    output.write(f'- ["{notation}", "{v1}", "{v2}"]\n')
                elif notation == "rest":
                    output.write(f'- ["rest", "{v1}"]\n')

    output.close()


if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    else:
        print("python img_to_yaml music_score.png line_freq output.yaml")
