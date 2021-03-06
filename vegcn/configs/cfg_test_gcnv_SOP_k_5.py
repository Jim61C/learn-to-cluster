import os.path as osp

# data locations
prefix = './data/SOP_dedup_global'
prefix_test = './data/SOP_dedup_test_global'
train_name = 'part0_train'
test_name = 'part0_train'
knn = 5
knn_method = 'faiss'
th_sim = 0.  # cut edges with similarity smaller than th_sim

# if `knn_graph_path` is not passed, it will build knn_graph automatically
train_data = dict(
    feat_path=osp.join(prefix, 'features', '{}.bin'.format(train_name)),
    label_path=osp.join(prefix, 'labels', '{}.meta'.format(train_name)),
    knn_graph_path=osp.join(prefix, 'knns', train_name,
                            '{}_k_{}.npz'.format(knn_method, knn)),
    k=knn,
    is_norm_feat=True,
    th_sim=th_sim,
    conf_metric='s_nbr_fast')

test_data = dict(feat_path=osp.join(prefix_test, 'features',
                                    '{}.bin'.format(test_name)),
                 label_path=osp.join(prefix_test, 'labels',
                                     '{}.meta'.format(test_name)),
                 knn_graph_path=osp.join(prefix_test, 'knns', test_name,
                                         '{}_k_{}.npz'.format('faiss',
                                                              knn)),
                 k=knn,
                 is_norm_feat=True,
                 th_sim=th_sim,
                 conf_metric='s_nbr_fast')

# model
model = dict(type='gcn_v',
             kwargs=dict(feature_dim=512, nhid=1024, nclass=1, dropout=0.))

# training args
optimizer = dict(type='SGD', lr=0.1, momentum=0.9, weight_decay=1e-4)
optimizer_config = {}

total_epochs = 20000
lr_config = dict(policy='step',
                 step=[int(r * total_epochs) for r in [0.5, 0.8, 0.9]])

batch_size_per_gpu = 1
workflow = [('train_gcnv', 1)]

# testing args
use_gcn_feat = False
max_conn = 1
tau_0 = 0.8
tau = 0.85

metrics = ['pairwise', 'bcubed', 'nmi']

# misc
workers_per_gpu = 1

checkpoint_config = dict(interval=1000)

log_level = 'INFO'
log_config = dict(interval=1, hooks=[
    dict(type='TextLoggerHook'),
])
