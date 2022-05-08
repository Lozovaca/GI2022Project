FROM ubuntu:20.04
RUN apt-get update && apt-get install -y wget \
make \
gcc \
zlib1g-dev  \
python3 \
python3-pip
WORKDIR /opt
RUN wget https://sourceforge.net/projects/bio-bwa/files/bwa-0.7.15.tar.bz2
RUN tar xfj bwa-0.7.15.tar.bz2
WORKDIR /opt/bwa-0.7.15
RUN make
WORKDIR /opt
COPY . /opt/project
WORKDIR /opt/project
RUN pip install -r requirements.txt