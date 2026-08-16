import streamlit as st
import numpy as np
import pandas as pd
from solution import population_simulation, plot_experimental_data, data_analysis, normalisation_to_one

st.title("Inchoherent Rate Model Simulation")
st.markdown("**Density matrix formalism** solver with custom lifetimes and transitions. You will be requested to define the number of states 'n' (Hilbert space dimension up to 10) in your system, including a ground (sink) state. " \
"\n\n You can then assign a starting **Fock state vector |m⟩** (this could be the bright state in your system), the time domain for the simulation and rate constants with corresponding state transitions. " \
"\n\n The time-evolution is then simulated with **QuTiP's** Lindblad master equation solver using the 'LSODA' method.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("System Definition:")
    n = st.number_input("Hilbert space dimension (n):", min_value=2, value=3, max_value=10, step=1, help="How many states do you have in your system? Include the ground state here.")
    m = st.number_input("Initialy occupied state (m):", 
        min_value=0, 
        max_value=int(n - 1), 
        value=0, 
        step=1,
        help="Usually set to 0, assigns a population value of 1 to this state. This could be the bright state in your system."
    )
    CHUNK = 5
    for start_idx in range(0, int(n), CHUNK):
        chunk = range(start_idx, min(start_idx + CHUNK, int(n)))
        headers = [f"|{i}⟩" for i in chunk]
        pops = [1 if i == m else 0 for i in chunk]
        chunk_df = pd.DataFrame([pops], columns=headers)
        st.dataframe(chunk_df, hide_index=True, width="stretch")

with col2:
    st.subheader("Time domain:", anchor="center")
    time_unit = st.selectbox("Time Unit:", ["fs", "ps", "ns", "μs", "ms", "s"], index=2, help="Define the units of the simulation.")
    t_min = st.number_input(f"Starting time [{time_unit}]:", value=0.01, help="Starting time for your simulation. Minimum value 0.01.", min_value=0.00, format="%.2f")
    t_max = st.number_input(f"Ending time [{time_unit}]:", value=1000, help="Ending time for your simulation. Maximum value 1,000,000.", max_value=1000000)
    num_points = st.number_input("Number of Time Points:", min_value=100, value=1000, max_value=50000, step=10, help="Defines the number of points beetween min and max t. 1000 is standard. Max allowed 50000, please note this will slow down the simulation.")

st.divider()

st.subheader("Rate constants and state transitions '(|b⟩ → |a⟩)'")
st.caption("Click '+' at the bottom of the table to add more transitions. You can export the table as CSV by hovering over the top right corner and pressing the 'Download as CSV' option. Remove any transitions by selecting the left column next to the desired transition and in the top right press 'Delete row(s)'. Below are some examples of a non-radiative and ISC (inter-system crossing) transitions.")

example_transitions = pd.DataFrame([
    {"name": "Non-radiative decay: Singlet '|0⟩ → |2⟩'", "tau": 15, "a": 2, "b": 0},
    {"name": "ISC: Singlet → Triplet '|0⟩ → |1⟩'", "tau": 30, "a": 1, "b": 0}
]).astype({"tau": "float64"})

editable_df = st.data_editor(
    example_transitions,
    num_rows="dynamic",
    width="stretch",
    column_config={
        "name": st.column_config.TextColumn("Name of the constant (optional)", max_chars=250, help="You can name your constants and transitions here. Convenient if you want to export the table."),
        "tau": st.column_config.NumberColumn(f"Lifetime τ [{time_unit}]", min_value=0.001, format = "%.3f", help="Tau parameter (Rate = 1/τ)"),
        "a": st.column_config.NumberColumn("Target state (a)", min_value=0, max_value=n-1, step=1, help="What state recieves population?"),
        "b": st.column_config.NumberColumn("Source state (b)", min_value=0, max_value=n-1, step=1, help="What state loses population?"),
    }
)

st.divider()

experimental_import = st.toggle("[NEW] I have experimental data to compare!", value=True, help="Do you have experimental data to compare to the model? Toggle OFF if you just want to run a model.")

if experimental_import:
    st.write("Please upload you experimental data as a CSV file. Make sure that the first column includes your time data (of the same unit as above) and do NOT include any ground states here. Order the data as per you simulation selection above. ")
    imported = st.file_uploader("Upload a file (CSV):", type="csv")

    if imported is not None:
        imported_df = pd.read_csv(imported)
        column_check = len(imported_df.columns)

        if column_check != (n):
            st.error(f"Please upload a file that has the right number of columns, in this case {n}. Your file had {column_check}.")

        else:
            st.write("Uploaded data overview:")
            st.dataframe(imported_df, width="stretch")
            st.write("Your data plot (log/log):")

            normalisation_choice = st.toggle("[IMPORTANT] I need to normalise my data!", value=False, help="Is your experimental data normalised to the maximum value? You can look at the figure below, the highest data point value should be 1.")

            if normalisation_choice:
                imported_df = normalisation_to_one(imported_df)
                fig_exp_norm = plot_experimental_data(imported_df)
                st.pyplot(fig_exp_norm)

            else:
                fig_exp = plot_experimental_data(imported_df)
                st.pyplot(fig_exp)
            
            col_run2, col_opt2 = st.columns([2, 1])
            st.divider()
            with col_opt2:
                show_ground_state = st.checkbox(f"Show 'ground state' |{int(n-1)}⟩ on plot?", value=False, help = "Usually left OFF here")

            with col_run2:
                run_pressed = st.button("Calculate and Compare with experiment (Run)", type="primary", width="stretch")

            if run_pressed:
                transitions = editable_df.to_dict(orient="records")
                with st.spinner("Solving..."):
                    t_list = np.logspace(np.log10(t_min), np.log10(t_max), int(num_points))
                    fig_model,fig_comparison,data_model,residuals = data_analysis(imported_df, n, m, transitions, t_list)
                    st.subheader("Model Results:")

                    st.pyplot(fig_model)
                    st.subheader("Per-state residuals:")
                    st.pyplot(fig_comparison)

                    user_file_name = st.text_input("**Enter file name for the model data:**", f"TADF_population_simulation_in_{time_unit}.csv", help="You can choose how to name your data here. The CSV will include your selected time unit in the column header.")
                    csv_data = data_model.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"Download model results as CSV (in {time_unit})",
                        data=csv_data,
                        file_name=user_file_name,
                        mime="text/csv"
                    )
                    user_file_name2 = st.text_input("**Enter file name for the residual data:**", f"TADF_residuals.csv", help="You can choose how to name your residuals data here.")
                    csv_data2 = residuals.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"Download resiudal results as CSV (in {time_unit})",
                        data=csv_data2,
                        file_name=user_file_name2,
                        mime="text/csv"
                    )


else:
    col_run, col_opt = st.columns([2, 1])

    with col_opt:
        show_ground_state = st.checkbox(f"Show 'ground state' |{int(n-1)}⟩ on plot?", value=False)

    with col_run:
        run_pressed = st.button("Calculate (Run)", type="primary", width="stretch")

    if run_pressed:
        transitions = editable_df.to_dict(orient="records")
        with st.spinner("Solving..."):
            t_list = np.logspace(np.log10(t_min), np.log10(t_max), int(num_points))
            fig, df_result = population_simulation(n, m, transitions, t_list)
            st.subheader("Results:")
            st.pyplot(fig)

            user_file_name = st.text_input("Enter file name:", f"TADF_population_simulation_in_{time_unit}.csv", help="You can choose how to name your data here. The CSV will include your selected time unit in the column header.")
            csv_data = df_result.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"Download results as CSV (in {time_unit})",
                data=csv_data,
                file_name=user_file_name,
                mime="text/csv"
            )