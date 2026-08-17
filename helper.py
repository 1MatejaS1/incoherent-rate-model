import matplotlib.pyplot as plt

def plot_experimental_data(data_exp):
    time_exp = data_exp.iloc[:, 0].values
    y_columns = data_exp.columns[1:]
    colors = plt.colormaps['tab10'].colors
    markerstyles = ['o', '^', 'x', 'v', 's', '*', 'P,', 'D', '>'] 

    fig, ax = plt.subplots()

    for i,col in enumerate(y_columns):
        ax.loglog(time_exp, data_exp[col], label=col, marker = markerstyles[i], linestyle = "None", color=colors[i])

    return fig

def normalisation_to_one(data_exp):

    y = data_exp.columns[1:]

    normalisation = data_exp.iloc[:, 1:].max()
    normalised = data_exp.copy()
    normalised[y] = data_exp[y] / normalisation

    return normalised