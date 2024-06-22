```bash
# os
ubuntu 18.04 or 20.04 or 22.04
```

```bash
# system
sudo apt-get install git tree
sudo apt-get install zstd flex bison gcc build-essential python3-pip
sudo apt-get install python3-setuptools python3-dev libssl-dev

# install conda
cd ~/alphabet/charm/
git clone https://github.com/xuehuan-yang/VFPPBA.git
git clone https://github.com/xuehuan-yang/PSME.git

cd ~/alphabet/software/
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
bash Anaconda3-2021.11-Linux-x86_64.sh 
(-> ENTER*100times -> yes -> PREFIX=/home/apollo/anaconda3)
source ~/.bashrc

# create conda env
conda create -n charm python=3.6
conda activate charm
conda install -c anaconda pycrypto
conda install -c menpo opencv  
conda install -c conda-forge matplotlib
pip install pyparsing==2.4.6
```

```bash
# conda env
openssl-1.1.1n
gmp-6.2.1
pbc-0.5.14
charm: charm https://github.com/JHUISI/charm
python: 3.6.13
ubuntu: 18.04.6 LTS
IOT: raspberry pi 4
opencv: 3.4.2
pycrypto: 2.6.1
```

```bash
# openssl 
conda activate charm
cd ~/alphabet/charm/
wget https://www.openssl.org/source/openssl-1.1.1n.tar.gz
tar -zxvf openssl-1.1.1n.tar.gz
cd ~/alphabet/charm/openssl-1.1.1n/
./config
make 
sudo make install
dpkg -l | grep openssl

# gmp-6.2.1
conda activate charm
cd ~/alphabet/charm/
wget https://gmplib.org/download/gmp/gmp-6.2.1.tar.zst
tar -I zstd -xvf gmp-6.2.1.tar.zst
cd gmp-6.2.1/
./configure
make
make check
sudo make install
dpkg -l | grep gmp

# pbc-0.5.14
conda activate charm
cd ~/alphabet/charm/
wget http://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz
tar -xvf pbc-0.5.14.tar.gz
cd pbc-0.5.14/
./configure
make
sudo make install
sudo ldconfig
dpkg -l | grep pbc

# charm
conda activate charm
cd ~/alphabet/charm/
git clone https://github.com/JHUISI/charm.git
cd charm/
sudo ./configure.sh
sudo ./configure.sh --python=~/anaconda3/envs/charm/bin/python # important to use conda python instead of /usr/bin/python
# tips raspberry pi 4 need to add following lines with various platform:  vim ./configure.sh  -> add lin 239-241  
# x86_64|amd64)
#   cpu='x86_64'
# ;;
# aarch64|armv7l)
#   cpu='aarch64'
# ;;
make
sudo make install
sudo ldconfig /usr/local/lib64/ 
sudo ldconfig /usr/local/lib/

cd ~/alphabet/charm/
rm -rf openssl-1.1.1n.tar.gz
rm -rf gmp-6.2.1.tar.zst
rm -rf pbc-0.5.14.tar.gz

# ABE
conda activate charm
cd ~/alphabet/charm/
git clone https://github.com/sagrawal87/ABE.git
cd ABE/
pip install -e ./

```


```bash
# run sample
conda activate charm
cd ~/alphabet/charm/PSME/src/00_aibbme
python 00_aibbme.py
```