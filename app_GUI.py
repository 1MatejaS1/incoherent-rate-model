import streamlit as st
import numpy as np
import pandas as pd
from solution import population_simulation

st.title("Inchoherent Rate Model")

st.markdown("Density matrix formalism solver with custom lifetimes and transitions")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("System Definition")
    n = st.number_input("Hilbert space dimension (n):", min_value=2, value=3, max_value=10, step=1)
    m = st.number_input("Initialy occupied state (m):", 
        min_value=0, 
        max_value=int(n - 1), 
        value=0, 
        step=1,
        help="Usually 0, assigns a population value of 1 to this state"
    )
    CHUNK = 5
    for start_idx in range(0, int(n), CHUNK):
        chunk = range(start_idx, min(start_idx + CHUNK, int(n)))
        headers = [f"|{i}⟩" for i in chunk]
        pops = [1 if i == m else 0 for i in chunk]
        chunk_df = pd.DataFrame([pops], columns=headers)
        st.dataframe(chunk_df, hide_index=True, use_container_width=True)

with col2:
    st.subheader("Time domain", anchor="center")
    time_unit = st.selectbox("Time Unit:", ["fs", "ps", "ns", "μs", "ms", "s"], index=2)
    t_min = st.number_input(f"Starting time [{time_unit}]:", value=0.1)
    t_max = st.number_input(f"Ending time [{time_unit}]:", value=10.0)
    num_points = st.number_input("Number of Time Points:", min_value=100, value=1000, max_value=50000, step=10)

st.divider()

st.subheader("Rate constants and state transitions (|b (target⟩ → |a (source⟩)")
st.caption("Click '+' at the bottom of the table to add more transitions.")

example_transitions = pd.DataFrame([
    {"tau": 5, "a": 2, "b": 0},
])

editable_df = st.data_editor(
    example_transitions,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "tau": st.column_config.NumberColumn(r"Lifetime τ [{time_unit}]", min_value=0.0001, help="Tau parameter (Rate = 1/τ)"),
        "a": st.column_config.NumberColumn("Target state (a)", min_value=0, max_value=n-1, step=1),
        "b": st.column_config.NumberColumn("Source state (b)", min_value=0, max_value=n-1, step=1),
    }
)

st.divider()

col_run, col_opt = st.columns([2, 1])

with col_opt:
    show_ground_state = st.checkbox(f"Show ground state |{int(n-1)}⟩ on plot?", value=False)

with col_run:
    run_pressed = st.button("Calculate (Run)", type="primary", use_container_width=True)

if run_pressed:
    transitions = editable_df.to_dict(orient="records")
    with st.spinner("Solving..."):
        t_list = np.logspace(np.log10(t_min), np.log10(t_max), int(num_points))
        fig, df_result = population_simulation(n, m, transitions, t_list)
        st.subheader("Results:")
        st.pyplot(fig)
            
        csv_data = df_result.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download results as CSV ({time_unit})",
            data=csv_data,
            file_name=f"population_simulation_{time_unit}.csv",
            mime="text/csv"
        )