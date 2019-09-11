import seaborn as sns
import matplotlib.pyplot as plt
from helper import get_cols_by_dtype


# Univariate Methoden
def distplot(data, show_plt_immediately=True):
    sns.distplot(data)
    if show_plt_immediately:
        plt.show()


def distplots(dataframe, cols_to_include=None, cols_to_exclude=None, target_col_name=None, save_to_path=None, **kwargs):
    # Ermittle zu plottende Spalten
    cols_to_plot = get_cols_by_dtype(dataframe, cols_to_include=cols_to_include, cols_to_exclude=cols_to_exclude, dtype='numeric')
    
    if len(cols_to_plot) == 0:
        print('Keine numerischen Spalten in DataFrame. Es wird keine Korrelationsmatrix erstellt!')

    # Anzahl Zeilen und Spalten des Plots festlegen
    cols = _get_amount_of_cols(len(cols_to_plot))
    rows = _get_amount_of_rows(len(cols_to_plot), cols)

    fig, ax = plt.subplots(rows, cols, figsize = (5*cols, 4 * rows)) # subplots erzeugt wohl ein eienes Figureobjekt

    # Plots erstellen
    for i, col in enumerate(cols_to_plot):
        if i+1 == cols*rows+1: break # wenn i größer als die maximale Anzahl vorhandener Plots ist
        plt.subplot(rows, cols, i+1 ) #
        if target_col_name is not None:
            unique_target_labels = dataframe[target_col_name].unique()
            for label in unique_target_labels:
                try: n_bins = kwargs['bins']
                except: n_bins = None
                sns.distplot(dataframe[col][dataframe[target_col_name] == label], bins=n_bins, label=str(label))
            plt.legend()
                
        else:
            sns.distplot(dataframe[col])
    if save_to_path is not None:
        plt.savefig(save_to_path + '/distplots.png', format='png')
    plt.show()
    
def correlation_matrix(dataframe, cols_to_include=None, cols_to_exclude=None, target_col_name=None, save_to_path=None):
    # Ermittle zu plottende Spalten
    cols_to_plot = get_cols_by_dtype(dataframe, cols_to_include=cols_to_include, cols_to_exclude=cols_to_exclude, dtype='numeric')
    
    # Erstelle Heatmap mithilfe von Korrelationsmatrix
    fig = plt.figure()
    fig.set_figheight(0.2 * len(cols_to_plot))
    fig.set_figwidth(0.2 * len(cols_to_plot))
    
    sns.heatmap(dataframe[cols_to_plot].corr())
    plt.show()

def _get_amount_of_cols(n_plots):
    # Anzahl Zeilen und Spalten des Plots festlegen
    if n_plots > 8:
        cols = 3
    elif n_plots > 3:
        cols = 2
    elif n_plots <= 3:
        cols = 1
    return cols
        
def _get_amount_of_rows(n_plots, n_cols):
    return int(n_plots/n_cols)