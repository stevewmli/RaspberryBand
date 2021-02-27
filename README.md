# RaspberryBand
Raspberry Pi Control Musican
- control servo motor to play music on xylophone

# Python setup on Raspberry PI
sudo apt install -y python3-venv pigpiod libjbig0 libjpeg-dev liblcms2-2 libopenjp2-7 libtiff5 libwebp6 libwebpdemux2 libwebpmux3 libzstd1 libatlas3-base libgfortran5 git tmux

# Python3 Virtual Environment
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Setup - start here:
sudo pigpiod && source env/bin/activate

# reset motor
cd ~/py_ws/RaspberryBand 

# Test
python raspberry_band.py

# music conversion
python img_to_yaml.py png_name line_freq
 
# OMR model
Play Sheet Music with Python, OpenCV, and an Optical Music Recognition Model - Artical by Israel Ebonko
https://heartbeat.fritz.ai/play-sheet-music-with-python-opencv-and-an-optical-music-recognition-model-a55a3bea8fe

The OMR Model mentioned in the artical
https://grfia.dlsi.ua.es/primus/models/PrIMuS/Semantic-Model.zip

TensorFlow code to perform end-to-end Optical Music Recognition on monophonic scores through Convolutional Recurrent Neural Networks and CTC-based training
Utilize the logic proivded in the ctc_predict.py in the img_to_yaml.py
https://github.com/OMR-Research/tf-end-to-end