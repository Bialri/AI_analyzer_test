
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install cmake make gcc g++ flex bison libpcap-dev libssl-dev python2-dev swig zlib1g-dev sendmail net-tools wget -y


mkdir bro

wget https://github.com/zeek/zeek/releases/download/v2.6.1/bro-2.6.1.tar.gz

tar zxvf ./bro-2.6.1.tar.gz -C ./bro
rm ./bro-2.6.1.tar.gz
(cd ./bro/bro-2.6.1 && CC=gcc-9 CXX=g++-9 ./configure && make && sudo make install)

echo PATH=/usr/local/bro/bin:$PATH >> ~/.bashrc
sudo rm -r ./bro

git clone https://github.com/igstbagusdharmaputra/NSL-KDD.git

