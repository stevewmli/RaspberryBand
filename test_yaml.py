import yaml

with open('./songs/do_re_me.yaml') as f:
    notes = yaml.load(f, Loader=yaml.FullLoader)
    for n in notes:
        print(n)