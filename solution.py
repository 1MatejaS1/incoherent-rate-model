import qutip as qt; from qutip import basis, mesolve; import numpy as np; import matplotlib.pyplot as plt; import pandas as pd

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

    solve_all = mesolve(H, ket, t_list, c_ops, expectations)

    time_col_name = f"time [{time_unit}]"
    data_dictionary = {time_col_name: t_list}
    for label, pop in zip(labels, solve_all.expect):
        data_dictionary[label] = pop
    DF = pd.DataFrame(data_dictionary)

    fig, ax = plt.subplots(figsize=(10, 5))

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