# -*- coding: utf-8 -*-

# basic smoke test that makes sure pytorch+nccl is generally good

import torch

torch.cuda.nccl.all_gather([torch.zeros(5).cuda()], [torch.zeros(5).cuda()])
