# APRS to IRC Gateway via RTL-SDR

## Install RTL-SDR

```bash
sudo apt-get install libasound2-dev libudev-dev libax25 ax25-apps ax25-tools git-core git cmake libusb-1.0-0-dev build-essential
cd ~
cat <<EOF >no-rtl.conf
blacklist dvb_usb_rtl28xxu
blacklist rtl2832
blacklist rtl2830
EOF
sudo mv no-rtl.conf /etc/modprobe.d/
git clone git://git.osmocom.org/rtl-sdr.git
cd rtl-sdr/
mkdir build
cd build
cmake ../ -DINSTALL_UDEV_RULES=ON
make
sudo make install
sudo ldconfig
cd ~
sudo cp ./rtl-sdr/rtl-sdr.rules /etc/udev/rules.d/
sudo reboot
```

## Install Direwolf

```bash
git clone https://github.com/wb2osz/direwolf.git
cd direwolf
mkdir build && cd build
cmake ..
make -j4
sudo make install
make install-conf
```

## Radio stack

### Create config file

```bash
ACHANNELS 1
ADEVICE null null
CHANNEL 0

MYCALL CALLSIGN-10
#IGSERVER aunz.aprs2.net
#IGLOGIN <CALLSIGN> 23018

MODEM 1200
AGWPORT 8000
KISSPORT 8001

```

### Start radio stack

```bash
rtl_fm -f 144.80M - | direwolf -c ./dire_sdr.conf -r 24000 -D 1 -
```

or `chmod a+x aprs.sh` and `./aprs.sh`

## Run IRC Gateway

```shell
pip install kiss3 irc

KISS_HOST=localhost KISS_PORT=8001 IRC_HOST=irc.example.com IRC_PORT=6697 CHANNEL_NAME="#example" BOT_NICK=aprs python3 aprs.py
```
