Built with **Streamlit** and **QuTiP** to simulate open quantum system dynamics using state-to-state transition lifetimes ($\tau$) and Lindblad jump operators.

## Key Features

- **Flexible Hilbert Space:** Easily define total levels and initial occupied state index.
- **Physical Parameterisation:** Input decay processes via lifetimes ($\tau$) instead of raw rate constants.
- **Dynamic Transition Builder:** Interactively add an arbitrary number of state-to-state collapse channels.
- **Experimental Data Import:** Import your experimental data and compare it with the model. You will also be able to see per-state residual plots.
- **Custom Time Units:** Select between `fs`, `ps`, `ns`, `μs`, `ms`, and `s`.
- **Log-Log Population Plots:** Visualise population dynamics with options to filter/hide specific state trajectories.
- **CSV Data Export:** Save simulation output with unit-tagged headers for external analysis. Save your table of constants and transitions.

## Local Installation

### 1) Clone the repository
```bash
git clone [https://github.com/1MatejaS1/incoherent-rate-model.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
```
### 2) Set up a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
### 3) Install dependencies
```bash
pip install -r requirements.txt
```
### 4) Run the streamlit application
```bash
streamlit run app_GUI.py
```
