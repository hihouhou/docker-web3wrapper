#
# Web3wrapper Dockerfile
#
# https://github.com/
#

# Pull base image.
FROM debian:latest

MAINTAINER hihouhou < hihouhou@hihouhou.com >

# Update & install packages for dep
RUN apt-get update && \
    apt-get install -y python3 pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY web3_wrapper.py /tmp/web3_wrapper.py


CMD ["python3", "/tmp/web3_wrapper.py"]
