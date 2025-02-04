import ROOT
from ROOT import RooFit, RooRealVar, RooPoisson, RooArgSet, RooArgList, RooProdPdf, RooDataSet, RooFormulaVar

# POIs: Mu (signal strength), eficiencia de la señal y eficiencia del fondo
mu = RooRealVar("mu", "Signal Strength", 1.0, 0, 5)

# Procesos y parámetros de sección transversal y eficiencia
processes = {
    "wzp6_ee_nuenueH_Hbb_ecm365": {"sigma": 0.02181, "eff": 0.038},
    "wzp6_ee_numunumuH_Hbb_ecm365_vbf": {"sigma": 0.004814, "eff": 0.0081},
    "p8_ee_ZZ_ecm365": {"sigma": 0.6428, "eff": 0.0014},
    "p8_ee_WW_ecm365": {"sigma": 10.7165, "eff": 0.00022},
    "p8_ee_tt_ecm365": {"sigma": 0.800, "eff": 0.032},
    "wzp6_ee_nunuH_Hbb_ecm365": {"sigma": 0.004814, "eff": 0.0081}
}

# Definir variables de eficiencia como constantes
eff_vars = {p: RooRealVar(f"eff_{p}", f"Efficiency {p}", processes[p]["eff"], 0, 1) for p in processes}

# Luminosidad en fb^-1
Lumi = 3000  # 3 ab^-1

# Fijar la luminosidad como constante (si no quieres que varíe durante el ajuste)
Lumi_var = RooRealVar("Lumi", "Luminosidad", Lumi, Lumi, Lumi)
Lumi_var.setConstant(True)

# Fijar las eficiencias como constantes
for p in processes:
    eff_vars[p].setConstant(True)  # Si no quieres que se ajusten, mantenlos como constantes

# Cálculo del número esperado de eventos
N_exp_signal_formula = "mu * (sigma_wzp6_ee_nuenueH_Hbb_ecm365 * eff_wzp6_ee_nuenueH_Hbb_ecm365 + sigma_wzp6_ee_numunumuH_Hbb_ecm365_vbf * eff_wzp6_ee_numunumuH_Hbb_ecm365_vbf)"
N_exp_background_formula = "sigma_p8_ee_ZZ_ecm365 * eff_p8_ee_ZZ_ecm365 + sigma_p8_ee_WW_ecm365 * eff_p8_ee_WW_ecm365 + sigma_p8_ee_tt_ecm365 * eff_p8_ee_tt_ecm365 + sigma_wzp6_ee_nunuH_Hbb_ecm365 * eff_wzp6_ee_nunuH_Hbb_ecm365"

# Crear variables para los eventos esperados en la señal y el fondo
N_exp_signal = RooFormulaVar("N_exp_signal", "Expected signal events", N_exp_signal_formula, 
                             RooArgList(mu, eff_vars["wzp6_ee_nuenueH_Hbb_ecm365"], eff_vars["wzp6_ee_numunumuH_Hbb_ecm365_vbf"]))

N_exp_background = RooFormulaVar("N_exp_background", "Expected background events", N_exp_background_formula, 
                                 RooArgList(eff_vars["p8_ee_ZZ_ecm365"], eff_vars["p8_ee_WW_ecm365"], 
                                            eff_vars["p8_ee_tt_ecm365"], eff_vars["wzp6_ee_nunuH_Hbb_ecm365"]))

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
