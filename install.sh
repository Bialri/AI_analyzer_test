
apt-get update
apt-get upgrade
apt-get install cmake make gcc g++ flex bison libpcap-dev libssl-dev py-thon-dev swig zlib1g-dev sendmail net-tools wget -y

apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa

sudo apt install python3.11 -y

mkdir bro

wget ./bro/bro-2.6.1.tar.gz https://github.com/zeek/zeek/releases/download/v2.6.1/bro-2.6.1.tar.gz

tar zxvf bro-2.6.1.tar.gz
./bro-2.6.1/configure
cd ./bro-2.6.1
make
make install

# Вручную нужно добавить в PATH bro PATH=/usr/local/bro/bin:$PATH

cd ..
git clone https://github.com/igstbagusdharmaputra/NSL-KDD.git

