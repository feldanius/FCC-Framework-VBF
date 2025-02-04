import ROOT
from ROOT import RooFit, RooRealVar, RooPoisson, RooArgSet, RooArgList, RooProdPdf, RooDataSet

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

# Cálculo del número esperado de eventos
N_exp_signal = sum(processes[p]["sigma"] * Lumi * eff_signal_var for p in ["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365_vbf"])
N_exp_background = sum(processes[p]["sigma"] * Lumi * eff_background_var for p in ["p8_ee_ZZ_ecm365", "p8_ee_WW_ecm365", "p8_ee_tt_ecm365", "wzp6_ee_nunuH_Hbb_ecm365"])

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
print(f"Signal Efficiency: {eff_signal_var.getVal():.4f}")
print(f"Background Efficiency: {eff_background_var.getVal():.4f}")
print(f"N_exp_signal: {N_exp_signal.getVal():.4f}")
print(f"N_exp_background: {N_exp_background.getVal():.4f}")
