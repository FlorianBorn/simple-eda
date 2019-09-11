# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:48:35 2019

@author: bornf
"""

#%%
from hyperopt import fmin
from hyperopt import tpe
from hyperopt import Trials
from hyperparameter_tuning import hyperparameter_spaces
from timeit import default_timer as timer
from hyperopt import STATUS_OK
import csv
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import numpy as np
import pandas as pd
import lightgbm as lgb

def tune_lgbm_hyperparameters(X, y, model_params=None, folds=5, iterations=100):
    
    # Trials object to track progress
    #bayes_trials = Trials()
    if model_params == None:
        space = hyperparameter_spaces.lgbm_space
    else:
        space = model_params
    # Algorithm
    tpe_algorithm = tpe.suggest
    
    # File to save first results
    out_file = 'gbm_trials.csv'
    of_connection = open(out_file, 'w')
    writer = csv.writer(of_connection)
    
    # Write the headers to the file
    writer.writerow(['loss', 'params', 'iteration', 'estimators', 'train_time'])
    of_connection.close()
    
    # Keep track of evals
    global ITERATION
    ITERATION = 0
    
    #Objective Function
    def objective_function(hyperparameters):
        '''
        Nimmt als Parameter ein Dict aus Hyperparametern (Keys) und deren Ausprägungen (Values) entgegen
        returns: Metrik, die durch den Optimierungsalgorithmus minimiert werden soll
        '''
        global ITERATION
        ITERATION += 1
        kfold = StratifiedKFold(n_splits=folds, shuffle=True)
        oof = np.zeros(len(X))
        
        start = timer()
        
        for i, (train_idx, val_idx) in enumerate(kfold.split(X, y)):
            
            #train_set = lgb.Dataset(X.iloc[train_idx], label=y[train_idx])
            #val_set = lgb.Dataset(X.iloc[val_idx], label=y[val_idx])
            train_set = get_lgbm_dataset(X.iloc[train_idx], y[train_idx])
            val_set = get_lgbm_dataset(X.iloc[val_idx], y[val_idx])
            
            mdl = lgb.train(hyperparameters,
                            train_set,
                            valid_sets=[train_set, val_set],
                            early_stopping_rounds = 250,
                            num_boost_round = 10000,
                            verbose_eval=1000)
            
            oof[val_idx] = mdl.predict(X.iloc[val_idx], num_iteration=mdl.best_iteration)
        
        run_time = timer() - start
        
        # get information for evaluation
        loss = 1 - roc_auc_score(y, oof) 
        best_iteration = mdl.best_iteration
            
        #Write to the csv file ('a' means append)
        of_connection = open(out_file, 'a')
        writer = csv.writer(of_connection)
        writer.writerow([loss, hyperparameters, ITERATION, best_iteration, run_time])
            
        return {'loss': loss, 'hyperparameters': hyperparameters, 'iteration': ITERATION,
            'estimators': best_iteration, 
            'train_time': run_time, 'status': STATUS_OK}
    
    
    # Find hyperparameters
    return fmin(fn=objective_function, space=space, algo=tpe_algorithm, max_evals=iterations, trials=None, verbose=1)

def get_lgbm_dataset(X, y):
    return lgb.Dataset(X, label=y)

#%%
#tune_lgbm_hyperparameters('lgbm', X, y, None)    

#%%
def get_space(model):
    if model == 'lgbm': return hyperparameter_spaces.lgbm_space
    if model == 'cat_boost': return hyperparameter_spaces.cat_space
    
#%% Optimization algorithm
#from hyperopt import tpe

# Algorithm
#tpe_algorithm = tpe.suggest

#%% Minimize 
#from hyperopt import fmin


#argmin = fmin(fn=objective_function, space=space, algo=tpe_algorithm, max_evals=5, trials=None, verbose=1)
