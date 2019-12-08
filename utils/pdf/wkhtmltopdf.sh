sudo wget https://builds.wkhtmltopdf.org/0.12.1.3/wkhtmltox_0.12.1.3-1~bionic_amd64.deb
sudo dpkg -i wkhtmltox_0.12.1.3-1~bionic_amd64.deb
sudo apt-get install -f -y
sudo ln -s /usr/local/bin/wkhtmltopdf /usr/bin
sudo ln -s /usr/local/bin/wkhtmltoimage /usr/bin

sudo apt-get install fonts-droid-fallback ttf-dejavu fonts-freefont-ttf fonts-liberation ttf-ubuntu-font-family -y
