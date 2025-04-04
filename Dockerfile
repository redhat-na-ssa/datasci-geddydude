FROM nvcr.io/nvidia/pytorch:24.10-py3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y libaio-dev

WORKDIR /workspace

RUN git clone https://github.com/NVIDIA/nccl-tests.git && \
    cd nccl-tests && make

RUN git clone https://github.com/pytorch/examples.git pytorch-examples 

COPY ddp/requirements.txt ddp/

RUN pip install -r ddp/requirements.txt

COPY ddp/*.py ddp/

COPY *.sh ./
