# -*- coding: utf-8 -*-

# test whether MPI and NCCL>=2.20.5 can play nice together without mpirun launch

import torch
import torch.distributed as dist

dist.init_process_group(backend='nccl')
dist.new_group(backend='mpi')
