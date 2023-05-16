```bash
# os
ubuntu 18.04 or 20.04 or 22.04
```

```bash
sudo apt-get install git tree
sudo apt-get install zstd flex bison gcc build-essential python3-pip
sudo apt-get install python3-setuptools python3-dev libssl-dev


# install conda
cd ~/alphabet/charm/
git clone https://github.com/xuehuan-yang/VFPPBA.git

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
