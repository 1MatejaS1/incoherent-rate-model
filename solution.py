import qutip as qt; from qutip import basis, mesolve, SolverOptions; import numpy as np; import matplotlib.pyplot as plt; import pandas as pd; from scipy.interpolate import interp1d

def population_simulation(number_of_states: int, starting_state: int, state_transitions: list[dict], t_list: np.ndarray, time_unit: str = "ns", hide_ground_state: bool = True):
    ket = basis(number_of_states,starting_state)
    H = qt.qzero(number_of_states)

    c_ops = []
    for choice in state_transitions:
        tau = choice["tau"]
        a = choice["a"]
        b = choice["b"]
        if tau > 0:
            rate = 1.0 / tau
            lindblad_jump_operator = qt.basis(number_of_states, a) * qt.basis(number_of_states, b).dag()
            c_ops.append(np.sqrt(rate) * lindblad_jump_operator)
    
    expectations = [qt.fock_dm(number_of_states, i) for i in range(number_of_states)]
    labels = [f"State |{i}⟩" for i in range(number_of_states)]


    setting = {"method": "lsoda"}
    solve_all = mesolve(H, ket, t_list, c_ops, expectations, options=setting)

    time_col_name = f"time [{time_unit}]"
    data_dictionary = {time_col_name: t_list}
    for label, pop in zip(labels, solve_all.expect):
        data_dictionary[label] = pop
    DF = pd.DataFrame(data_dictionary)

    fig, ax = plt.subplots()

    states_to_plot = range(number_of_states - 1) if (hide_ground_state and number_of_states > 1) else range(number_of_states)
    colors = plt.colormaps['tab10'].colors
    styles = ['-', '--', '-.', ':']

    for i in states_to_plot:
        label = labels[i]
        style = styles[i % len(styles)]
        ax.loglog(DF[time_col_name], DF[label], label=label, color=colors[i], linestyle=style)

    ax.set_xlabel(f"Time [{time_unit}]", fontsize=12)
    ax.set_ylabel("Population [no units]", fontsize=12)
    ax.legend(loc="best")
    plt.tight_layout()

    return fig, DF

def plot_experimental_data(data_exp):
    time_exp = data_exp.iloc[:, 0].values
    y_columns = data_exp.columns[1:]
    colors = plt.colormaps['tab10'].colors
    markerstyles = ['o', '^', 'x', 'v', 's', '*', 'P,', 'D', '>'] 

    fig, ax = plt.subplots()

    for i,col in enumerate(y_columns):
        ax.loglog(time_exp, data_exp[col], label=col, marker = markerstyles[i], linestyle = "None", color=colors[i])

    return fig

def data_analysis(data_exp, number_of_states: int, starting_state: int, state_transitions: list[dict], t_list: np.ndarray, time_unit: str = "ns", hide_ground_state: bool = True):

    fig_model,data_model = population_simulation(number_of_states, starting_state, state_transitions, t_list, time_unit, hide_ground_state)

    time_exp = data_exp.iloc[:, 0].values
    time_model = data_model.iloc[:, 0].values

    residuals = pd.DataFrame(index=time_exp)
    residuals.index.name = data_exp.columns[0]

    for i in range(1, data_exp.shape[1]):
        state = data_exp.columns[i]
        state_data = data_exp.iloc[:, i].values
        state_model_data = data_model.iloc[:, i].values    
    
        model_interpolation = interp1d(time_model, state_model_data, kind='linear', fill_value="extrapolate")

        data_model_interpolate = model_interpolation(time_exp)
    
        residuals[state] = np.log10(state_data) - np.log10(data_model_interpolate)

    dimension = residuals.shape[1]

    fig_res, ax2 = plt.subplots(dimension, 1, squeeze=False, figsize=(10, 2.5 * dimension))
    colors = plt.colormaps['tab10'].colors

    for i in range(dimension):
        ax2[i, 0].axhline(y=0, color='k')
        ax2[i, 0].plot(residuals.iloc[:, i], marker = "x", linestyle = "None", color=colors[i]) 
        ax2[i, 0].set_ylabel(residuals.columns[i])
        ax2[i, 0].set_xscale('log')
        ax2[i, 0].set_ylabel("Residual")
        ax2[i, 0].set_xlabel(f"Time [{time_unit}]")

    plt.tight_layout()

    return fig_model, fig_res, data_model, residuals

def normalisation_to_one(data_exp):

    x = data_exp.columns[0]
    y = data_exp.columns[1:]

    normalisation = data_exp.iloc[:, 1:].max()
    normalised = data_exp.copy()
    normalised[y] = data_exp[y] / normalisation

    return normalised