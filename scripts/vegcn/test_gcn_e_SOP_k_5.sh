export CUDA_VISIBLE_DEVICES=$1
export PYTHONPATH=.

config=vegcn/configs/cfg_test_gcne_SOP_k_5.py

# test
load_from=data/work_dir/cfg_train_gcne_SOP_k_5/latest.pth
python vegcn/main.py \
    --config $config \
    --phase 'test' \
    --load_from $load_from \
    --save_output \
    --force