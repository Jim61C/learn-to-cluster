import os.path as osp
from mmcv import Config
from utils import rm_suffix
from vegcn.extract import extract_gcn_v

# data locations
prefix = './data/SOP_dedup_test_global'
test_name = 'part0_train'
knn = 5
knn_method = 'faiss'
th_sim = 0.  # cut edges with similarity smaller than th_sim

# gcn_v configs
_work_dir = 'work_dir'
ckpt_name = 'latest'
gcnv_cfg = './vegcn/configs/cfg_test_gcnv_SOP_k_5.py'
gcnv_cfg_name = rm_suffix(osp.basename(gcnv_cfg))
gcnv_cfg = Config.fromfile(gcnv_cfg)
gcnv_cfg.load_from = '{}/{}/{}/{}.pth'.format('data', _work_dir, 'cfg_train_gcnv_SOP_k_5',
                                              ckpt_name)

use_gcn_feat = False
gcnv_prefix = '{}/{}/{}/{}_gcnv_k_{}_th_{}'.format('data', _work_dir,
                                                   gcnv_cfg_name, test_name,
                                                   gcnv_cfg.knn,
                                                   gcnv_cfg.th_sim)
if use_gcn_feat:
    gcnv_nhid = gcnv_cfg.model.kwargs.nhid
    feat_path = osp.join(gcnv_prefix, 'features', '{}.bin'.format(ckpt_name))
else:
    gcnv_nhid = gcnv_cfg.model.kwargs.feature_dim
    feat_path = osp.join(prefix, 'features', '{}.bin'.format(test_name))

pred_conf_path = osp.join(gcnv_prefix, 'pred_confs',
                                     '{}.npz'.format(ckpt_name))
extract_gcn_v(feat_path, pred_conf_path, 'test_data', gcnv_cfg)

# testing args
max_conn = 1
tau = 0.8

metrics = ['pairwise', 'bcubed', 'nmi']

# if `knn_graph_path` is not passed, it will build knn_graph automatically
test_data = dict(feat_path=feat_path,
                 label_path=osp.join(prefix, 'labels',
                                     '{}.meta'.format(test_name)),
                 pred_confs=pred_conf_path,
                 k=knn,
                 is_norm_feat=True,
                 th_sim=th_sim,
                 max_conn=max_conn,
                 ignore_ratio=0.8)

# model
regressor = False
nclass = 1 if regressor else 2
model = dict(type='gcn_e',
             kwargs=dict(feature_dim=gcnv_nhid,
                         nhid=1024,
                         nclass=nclass,
                         dropout=0.))

batch_size_per_gpu = 1

# misc
workers_per_gpu = 1

log_level = 'INFO'
log_config = dict(interval=200, hooks=[
    dict(type='TextLoggerHook'),
])
