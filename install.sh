
apt-get update
apt-get upgrade
apt-get install cmake make gcc g++ flex bison libpcap-dev libssl-dev python-dev swig zlib1g-dev sendmail net-tools wget -y


mkdir bro

wget https://github.com/zeek/zeek/releases/download/v2.6.1/bro-2.6.1.tar.gz

tar zxvf ./bro-2.6.1.tar.gz -C ./bro
(cd ./bro && ./configure && make && make install)


# Вручную нужно добавить в PATH bro PATH=/usr/local/bro/bin:$PATH

git clone https://github.com/igstbagusdharmaputra/NSL-KDD.git

