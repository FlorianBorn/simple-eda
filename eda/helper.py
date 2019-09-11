import pandas as pd

NUMERICAL_DTYPES = ['float64',
                    'float32',
                    'float16',
                    'int64',
                    'int32',
                    'int16'
                    ]


def get_cols_by_dtype(dataframe, cols_to_include=None, cols_to_exclude=None, dtype=None):
	if dtype == 'numeric':
		dtypes = NUMERICAL_DTYPES
	elif dtype == None:
		dtypes = ['']
	# ToDo: andere Datentypen einfügen

	if cols_to_exclude is None:
		cols_to_exclude = ['']

	# Wenn die zu nutzenden Spalten angegeben sind
	if cols_to_include is not None:
		cols_to_plot = [col for col in cols_to_include if col not in cols_to_exclude] # keine Prüfung, ob Spalten Zahlen sind
	# Wenn nichts angegeben ist...
	# 	nimm alle Spalten entsprechend des angegebenen Datentypes (alle wenn keiner angegeben ist)
	# 	ignoriere 'exclude' Spalten 
	else:
		cols_to_plot = [col for col in dataframe.columns
						if dataframe[col].dtype in dtypes and col not in cols_to_exclude]
	return cols_to_plot