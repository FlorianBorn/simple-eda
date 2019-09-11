# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 22:50:02 2019

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
import catboost as cat

def get_catboost_dataset(X, y):
    return cat.Pool(X, label=y)

def tune_catboost_hyperparameters(X, y, model_params=None, folds=5, loss_function='RMSE', iterations=100):
    '''
    loss_function determines which ml problem to solve!
    
    '''
    
    # Trials object to track progress
    #bayes_trials = Trials()
    if model_params == None:
        space = hyperparameter_spaces.cat_space
    else:
        space = model_params
    space['loss_function'] = loss_function
        
    # Algorithm
    tpe_algorithm = tpe.suggest
    
    # File to save first results
    out_file = 'cat_trials.csv'
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
        
        print("--------------------")
        print(hyperparameters)
        print("--------------------")
        
        bootstrap_type = hyperparameters['bootstrap_type']['bootstrap_type']
        subsample = hyperparameters['bootstrap_type'].get('subsample')
        if subsample is not None:
            hyperparameters['subsample'] = subsample
        hyperparameters['bootstrap_type'] = bootstrap_type
        
        start = timer()
        
        for i, (train_idx, val_idx) in enumerate(kfold.split(X, y)):
            
            train_set = get_catboost_dataset(X.iloc[train_idx], y[train_idx])
            val_set = get_catboost_dataset(X.iloc[val_idx], y[val_idx])
            
            #mdl = cat.CatBoost(hyperparameters)
            mdl = cat.CatBoostClassifier(**hyperparameters)
            mdl.fit(train_set, 
                    #eval_set=[train_set
                    #          , val_set],
                    eval_set = val_set,
                    early_stopping_rounds = 250,
                    )
            
            oof[val_idx] = mdl.predict_proba(X.iloc[val_idx])[:,1]
        
        run_time = timer() - start
        
        # get information for evaluation
        loss = 1 - roc_auc_score(y, oof) 
        best_iteration = mdl.get_best_iteration()
            
        #Write to the csv file ('a' means append)
        of_connection = open(out_file, 'a')
        writer = csv.writer(of_connection)
        writer.writerow([loss, hyperparameters, ITERATION, best_iteration, run_time])
            
        return {'loss': loss, 'hyperparameters': hyperparameters, 'iteration': ITERATION,
            'estimators': best_iteration, 
            'train_time': run_time, 'status': STATUS_OK}
    
    
    # Find hyperparameters
    return fmin(fn=objective_function, space=space, algo=tpe_algorithm, max_evals=iterations, trials=None, verbose=1)