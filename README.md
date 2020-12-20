# RaspberryBand
Raspberry Pi Control Musican
- control servo motor to play music on xylophone

# Python setup on Raspberry PI
sudo apt install -y python3-venv pigpiod libjbig0 libjpeg-dev liblcms2-2 libopenjp2-7 libtiff5 libwebp6 libwebpdemux2 libwebpmux3 libzstd1 libatlas3-base libgfortran5 git tmux

# Python3 Virtual Environment
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Setup:
sudo pigpiod && source env/bin/activate

# Test
python raspberry_band.py