[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Built with **Streamlit** and **QuTiP** to simulate open quantum system dynamics using state-to-state transition lifetimes ($\tau$) and Lindblad jump operators. This is a **density matrix formalism** solver with custom lifetimes and transitions. You will be requested to define the number of states 'n' (Hilbert space dimension up to 10) in your system, including a ground (sink) state. You can then assign a starting **Fock state vector |m⟩** (this could be the bright state in your system), the time domain for the simulation and rate constants with corresponding state transitions. The time evolution is then simulated with **QuTiP's Lindblad master equation** solver using the **'LSODA'** method. 

If you are looking to review this code, the main solver logic is located in the **solution.py** script.

## Key Features

- **Flexible Hilbert Space:** Easily define the total number of levels and the initially occupied state.
- **Physical Parameterisation:** Input decay processes via lifetimes ($\tau$) instead of raw rate constants. Save your table of constants and transitions.
- **Dynamic Transition Builder:** Interactively add an arbitrary number of state-to-state collapse channels.
- **Experimental Data Import:** Import your experimental data and compare it with the model. You will also be able to see per-state residual plots.
- **Custom Time Units:** Select between `fs`, `ps`, `ns`, `μs`, `ms`, and `s`.
- **Log-Log Population Plots:** Visualise population dynamics with options to filter/hide specific state trajectories.
- **CSV Data Export:** Save simulation output with unit-tagged headers for external analysis.

## Local Installation Using Git (Recommended):

### 1) Clone the repository
```bash
git clone [https://github.com/1MatejaS1/incoherent-rate-model.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
```
### 2) Set up a virtual environment

**Windows (Command Prompt / PowerShell):**
```bash
python -m venv .venv
.venv\Scripts\activate
```
**Linux / macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```
### 3) Install dependencies
```bash
pip install -r requirements.txt
```
### 4) Run the streamlit application
```bash
streamlit run app_GUI.py
```

## Without Git (Download ZIP):

### 1) Download the files:

- At the top of this GitHub repository page, click the **green < > Code button**. Select **Download ZIP**.
- Extract the downloaded .zip file to a location on your computer.
- Open your terminal or command prompt in the extracted folder:

**Windows:** Open the extracted folder in File Explorer, click the address bar, type cmd, and press Enter.

**macOS:** Right-click the extracted folder, hover over Services, and select New Terminal at Folder.

### 2) Run the code:

Once you are inside the project directory in your terminal/command prompt:

- Set up a virtual environment

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

 - Install dependencies

```bash
pip install -r requirements.txt
```

- Run the Streamlit application

```bash
streamlit run app_GUI.py
```
