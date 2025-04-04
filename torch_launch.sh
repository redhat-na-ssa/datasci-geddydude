#!/usr/bin/bash

set -x

# launcher script for a pod that is assumed to have been
# mutated with all necessary NCCL and other env vars

LOGLEVEL="DEBUG"

NUM_GPU=$(nvidia-smi -L | wc -l)

# check if we are MN distributed or not
if [[ -z "${PET_NNODES}" ]]; then
	PET_NNODES=1
	MASTER_ADDR=localhost
	MASTER_PORT=1234
fi

torchrun \
    --nnodes=$PET_NNODES:$PET_NNODES\
    --nproc_per_node=$NUM_GPU\
    --max_restarts=3\
    --rdzv_id=1\
    --rdzv_backend=c10d\
    --rdzv_endpoint="$MASTER_ADDR:$MASTER_PORT"\
    --master_addr="$MASTER_ADDR" \
    --master_port=$MASTER_PORT \
    $@
