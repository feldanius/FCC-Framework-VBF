import ROOT
from ROOT import RooFit, RooRealVar, RooPoisson, RooArgSet, RooDataSet, RooFormulaVar, RooArgList

# Luminosidad en fb^-1
Lumi = 3000  # 3 ab^-1

# POIs: Mu (signal strength), eficiencia de la señal y eficiencia del fondo
mu = RooRealVar("mu", "Signal Strength", 1.0, 0, 5)

# Cross-sections en pb y eficiencias
processes = {
    "wzp6_ee_nuenueH_Hbb_ecm365": {"sigma": 0.02181, "eff": 0.038},
    "wzp6_ee_numunumuH_Hbb_ecm365_vbf": {"sigma": 0.004814, "eff": 0.0081},
    "p8_ee_ZZ_ecm365": {"sigma": 0.6428, "eff": 0.0014},
    "p8_ee_WW_ecm365": {"sigma": 10.7165, "eff": 0.00022},
    "p8_ee_tt_ecm365": {"sigma": 0.800, "eff": 0.032},
    "wzp6_ee_nunuH_Hbb_ecm365": {"sigma": 0.004814, "eff": 0.0081}
}

# Crear un diccionario de variables RooRealVar para las eficiencias
eff_vars = {p: RooRealVar(f"eff_{p}", f"Efficiency {p}", processes[p]["eff"], 0, 1) for p in processes}

# Crear una lista de términos para la fórmula de N_exp_signal
signal_terms = [f"{processes[p]['sigma']}*{Lumi}*eff_{p}" for p in ["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365_vbf"]]

# Definir una variable de fórmula para N_exp_signal
N_exp_signal_formula = "+".join(signal_terms)
N_exp_signal = RooFormulaVar("N_exp_signal", "Expected signal events", N_exp_signal_formula, RooArgList(mu, *[eff_vars[p] for p in ["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365_vbf"]]))

# Crear una lista de términos para la fórmula de N_exp_background
background_terms = [f"{processes[p]['sigma']}*{Lumi}*eff_{p}" for p in ["p8_ee_ZZ_ecm365", "p8_ee_WW_ecm365", "p8_ee_tt_ecm365", "wzp6_ee_nunuH_Hbb_ecm365"]]

# Definir una variable de fórmula para N_exp_background
N_exp_background_formula = "+".join(background_terms)
N_exp_background = RooFormulaVar("N_exp_background", "Expected background events", N_exp_background_formula, RooArgList(mu, *[eff_vars[p] for p in ["p8_ee_ZZ_ecm365", "p8_ee_WW_ecm365", "p8_ee_tt_ecm365", "wzp6_ee_nunuH_Hbb_ecm365"]]))

# Número total de eventos esperados con mu
N_exp_total = RooRealVar("N_exp_total", "Expected total events", 0, 1e6)
N_exp_total.setVal(mu.getVal() * N_exp_signal.getVal() + N_exp_background.getVal())

# Número de eventos observados
N_obs = 191371.2  # Valor real obtenido
N_obs_var = RooRealVar("N_obs", "Número de eventos observados", N_obs, 0, 1e6)

# Likelihood de Poisson
likelihood = RooPoisson("likelihood", "Poisson Likelihood", N_obs_var, N_exp_total)

# Crear un dataset vacío para el ajuste
data = RooDataSet("data", "data", RooArgSet(N_obs_var))

# Ajuste con los POIs
fit_result = likelihood.fitTo(data, RooFit.Save())

# Imprimir resultados
print(f"Mu (Signal Strength): {mu.getVal():.4f}")
for p in processes:
    print(f"Efficiency for {p}: {eff_vars[p].getVal():.4f}")
print(f"N_exp_signal: {N_exp_signal.getVal():.4f}")
print(f"N_exp_background: {N_exp_background.getVal():.4f}")
