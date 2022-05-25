```bash
#!/bin/bash

# packages
sudo apt install zstd
sudo apt-get install flex
sudo apt-get install bison
sudo apt-get install gcc build-essential
sudo apt-get install python3-setuptools
sudo apt-get install python3-dev
sudo apt-get install python3-pip
pip3 install numpy

# conda
conda install -c anaconda pycrypto


# openssl 
# https://www.openssl.org/source/gitrepo.html
git clone git://git.openssl.org/openssl.git
wget https://www.openssl.org/source/openssl-1.1.1n.tar.gz
tar -zxvf openssl-1.1.1n.tar.gz
cd /home/apollo/openssl
./config
make 
sudo make install
dpkg -l | grep openssl


# gmp-6.2.1
# https://gmplib.org/manual/Installing-GMP
cd /home/apollo/software/charm
wget https://gmplib.org/download/gmp/gmp-6.2.1.tar.zst
tar -I zstd -xvf gmp-6.2.1.tar.zst
cd gmp-6.2.1/
./configure
make
make check
sudo make install
dpkg -l | grep gmp


# pbc-0.5.14
# https://crypto.stanford.edu/pbc/manual/ch01.html
cd /home/apollo/software/charm
wget http://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz
tar -xvf pbc-0.5.14.tar.gz
cd pbc-0.5.14/
./configure
make
sudo make install
sudo ldconfig
# lib3.so can not find it 
sudo ldconfig /usr/local/lib64/
dpkg -l | grep pbc


