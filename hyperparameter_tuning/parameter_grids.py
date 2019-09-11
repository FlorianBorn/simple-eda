
params_SVC = {
	'C': [0.001, 0.01, 0.1, 1.0, 10, 20, 50, 100],
	'kernel': ['rbf', 'linear', 'poly', 'sigmoid'],
	'probability': [True],
	'class_weight': ['balanced', None],
	'tol': [1e-2, 1e-3, 1e-4],
	'random_state': [42],
	'verbose': [1]
}

params_DecisionTreeClassifier = {
	'criterion': ['gini', 'entropy'],
	'splitter': ['best', 'random'],
	'max_depth': [2,3,4,5,7,10,15],
	'min_samples_split': [2, 5, 10],
	'min_samples_leaf': [1,2,4,20],
	'max_features': [10, 50, 100, 250],
	'random_state': [42],
	#'verbose': [1] # verbose gibt es nicht für Decision Trees!
}

params_ElasticNet = {
	'alpha': [0.1, 0.25, 0.6, 1, 2, 10],
	'l1_ratio': [0.1, 0.25, 0.5, 0.75, 0.9],
	'normalize': [True, False],
	'random_state': [42]
}

params_LogisticRegression = {
	'penalty': ['l1', 'l2'],
	'tol': [1e-5, 1e-4, 1e-3],
	'C': [0.001, 0.01, 0.1, 1.0, 10, 20, 50, 100],
	'class_weight': ['balanced', None],
	'random_state': [42],
	#'solver': ['lbfgs', 'liblinear'],
	'n_jobs': [-1]
}

params_Lasso = {
	'alpha': [0, 0.1, 0.2, 0.5, 0.75, 1, 1.5, 2, 5],
	'fit_intercept': [True],
	'normalize': [True, False],
	'tol': [1e-5, 1e-4, 1e-3, 1e-2],
	'max_iter': [100],
	'random_state': [42]
	}