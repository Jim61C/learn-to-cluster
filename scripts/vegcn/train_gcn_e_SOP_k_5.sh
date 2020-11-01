export CUDA_VISIBLE_DEVICES=$1
export PYTHONPATH=.

cfg_name=cfg_train_gcne_SOP_k_5
config=vegcn/configs/$cfg_name.py


# train
python vegcn/main.py \
    --config $config \
    --phase 'train'
