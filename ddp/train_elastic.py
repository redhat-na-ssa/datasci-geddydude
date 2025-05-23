# -*- coding: utf-8 -*-

# distributed ToyModel 

import argparse
import os
import sys
import time
import tempfile
from urllib.parse import urlparse

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim

from torch.nn.parallel import DistributedDataParallel as DDP

class ToyModel(nn.Module):
    def __init__(self):
        super(ToyModel, self).__init__()
        self.net1 = nn.Linear(10, 10)
        self.relu = nn.ReLU()
        self.net2 = nn.Linear(10, 5)

    def forward(self, x):
        return self.net2(self.relu(self.net1(x)))

def train():
    local_rank = int(os.environ["LOCAL_RANK"])
    rank = int(os.environ["RANK"])
    print(f"[{os.getpid()}] (rank = {rank}, local_rank = {local_rank}) training...")
    model = ToyModel().cuda(local_rank)
    ddp_model = DDP(model, [local_rank])

    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.001)
    epoch = 100
    for i in range(epoch):
        time.sleep(1)
        optimizer.zero_grad()
        outputs = ddp_model(torch.randn(20, 10).to(local_rank))
        labels = torch.randn(20, 5).to(local_rank)
        loss = loss_fn(outputs, labels)
        loss.backward()
        print(f"[{os.getpid()}] epoch {i} (rank = {rank}, local_rank = {local_rank}) loss = {loss.item()}\n")
        optimizer.step()

def run():
    env_dict = {
        key: os.environ[key]
        for key in ("MASTER_ADDR", "MASTER_PORT", "WORLD_SIZE", "LOCAL_WORLD_SIZE")
    }
    print(f"[{os.getpid()}] Initializing process group with: {env_dict}")

    dist.init_process_group(backend="nccl")
    train()
    dist.destroy_process_group()


if __name__ == "__main__":
    run()
