# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:31:44 2019

@author: bornf
"""
 #%%
from hyperopt import hp
from hyperopt.pyll.base import scope
import numpy as np

'''
Hier werden alle Hyperparamete, die Optimiert werden sollen sammt Suchdomain angegeben
Die Hyperparameter werden in einem Dict angegeben. Schema: {'Hyperparameter': Verteilung der Parameter oder Auswahl}
'''
lgbm_space = {
        'boosting': hp.choice('boosting', ['gbdt', 'dart']),
        'learning_rate': hp.loguniform('learning_rate', np.log(0.01), np.log(0.2) ),
        'num_leaves': scope.int(hp.quniform('num_leaves', 2, 40, 1)),
        'max_leaf': scope.int(hp.quniform('max_leaf', 6, 200, 5)),
        'max_depth': scope.int(hp.quniform('max_depth', 2, 20, 1)),
        'min_data_in_leaf': scope.int(hp.quniform('min_data_in_leaf', 10, 30, 2)),
        'min_sum_hessian_in_leaf': hp.loguniform('min_sum_hessian_in_leaf', 1e-4, 1e-2),
        'min_sum_hessian_per_leaf': hp.loguniform('min_sum_hessian_per_leaf', 1e-4, 1e-2),
        'bagging_fraction': hp.uniform('bagging_fraction', 0.0, 1.0),
        'bagging_freq': scope.int(hp.quniform('bagging_freq', 0, 100, 10)),
        'feature_fraction': hp.uniform('feature_fraction', 0.7, 1),
        'feature_fraction_seed': 1337,
        'early_stopping_rounds': 150,
        'metric_types': ['auc'],
        'seed':  1337,
        'n_jobs': 4,
        'lambda_l1': hp.uniform('lambda_l1', 0.0, 1.0),
        'lambda_l2': hp.uniform('lambda_l2', 0.0, 1.0)
        } 

# https://catboost.ai/docs/concepts/python-reference_parameters-list.html
cat_space = {
        'iterations': 15000,
        'learning_rate': hp.loguniform('learning_rate', np.log(0.01), np.log(0.2)),
        'random_seed': 1337,
        'l2_leaf_reg': hp.uniform('l2_leaf_ref', 0.5, 20),
        'bootstrap_type': hp.choice('bootstrap_type', [{'bootstrap_type': 'Bayesian'}, #https://towardsdatascience.com/automated-machine-learning-hyperparameter-tuning-in-python-dfda59b72f8a
                                                       {'bootstrap_type': 'Bernoulli', 
                                                            'subsample': hp.uniform('subsample', 0.2, 0.9 )}]),
        #'sampling_frequency': hp.choice('sampling_frequency', ['PerTree', 'PerTreeLevel']),
        'random_strength': hp.normal('random_strength', 1, 0.5),
        #bagging_temperature
        'use_best_model': True,
        'max_depth': scope.int(hp.quniform('max_depth', 2, 6, 1)),
        #'rsm': hp.uniform('rsm', 0.5, 1.0),
        #nan_mode
        #fold_permutation_block_size
        'scale_pos_weight': hp.choice('scale_pos_weight', [1, 9]),
        #'max_bin': 
        'early_stopping_rounds': 400,
        'verbose': 500,
        'used_ram_limit': 16 * 10**9,
        'gpu_ram_part': 0.95
        #'thread_count': -1
        }
