import ROOT
import os

# Function to load histograms from multiple ROOT files
def load_histograms(file_list, hist_name):
    """
    Load and combine histograms from multiple ROOT files.

    Args:
        file_list (list of str): List of ROOT file paths.
        hist_name (str): Name of the histogram to extract.

    Returns:
        ROOT.TH1F: Combined histogram from all files.
    """
    combined_hist = None

    for file_name in file_list:
        file = ROOT.TFile.Open(file_name)
        if not file or file.IsZombie():
            print(f"Error: Unable to open {file_name}")
            continue

        hist = file.Get(hist_name)
        if not hist:
            print(f"Error: Histogram {hist_name} not found in {file_name}")
            continue

        if combined_hist is None:
            combined_hist = hist.Clone(f"combined_{hist_name}")
            combined_hist.SetDirectory(0)
        else:
            combined_hist.Add(hist)

        file.Close()

    return combined_hist

# Function to define the Double-Sided Crystal Ball (DSCB) function
def define_dscb_model(variable):
    """
    Define a Double-Sided Crystal Ball (DSCB) model for the signal using RooGenericPdf.
    """
    mean = ROOT.RooRealVar("mean", "Mean of DSCB", 125, 120, 130)
    sigma = ROOT.RooRealVar("sigma", "Width of DSCB", 2, 0.1, 5)
    alphaL = ROOT.RooRealVar("alphaL", "Alpha Left", 1.5, 0.1, 5)
    alphaR = ROOT.RooRealVar("alphaR", "Alpha Right", 1.5, 0.1, 5)
    nL = ROOT.RooRealVar("nL", "Power Left", 2, 0.1, 10)
    nR = ROOT.RooRealVar("nR", "Power Right", 2, 0.1, 10)

    # Define the DSCB function as a RooGenericPdf
    formula = """
    (abs(@0-@1)/@2 <= @3) * exp(-0.5*((@0-@1)/@2)^2) +
    (abs(@0-@1)/@2 > @3 && @0 < @1) * exp(-0.5*@3^2) * (1 + (@3 - abs(@0-@1)/@2)/@4)^(-@4) +
    (abs(@0-@1)/@2 > @3 && @0 > @1) * exp(-0.5*@3^2) * (1 + (@3 - abs(@0-@1)/@2)/@5)^(-@5)
    """
    dscb = ROOT.RooGenericPdf(
        "dscb", "Double-Sided Crystal Ball", formula,
        ROOT.RooArgList(variable, mean, sigma, alphaL, nL, alphaR, nR)
    )
    return dscb


# Function to define a polynomial model for the background
def define_polynomial_model(variable):
    """
    Define a first-degree polynomial model for the background.

    Args:
        variable (RooRealVar): The variable to model.

    Returns:
        RooAbsPdf: The polynomial model.
    """
    c0 = ROOT.RooRealVar("c0", "Constant Term", 0, -10, 10)
    c1 = ROOT.RooRealVar("c1", "Linear Term", 0, -10, 10)

    background = ROOT.RooPolynomial("background", "Background Model", variable, ROOT.RooArgList(c0, c1))
    return background

# Main function to perform the analysis
def main():
    # Output directory
    outdir = "/eos/user/f/fdmartin/FCC365_histograms/signal_strenght"
    os.makedirs(outdir, exist_ok=True)

    # Input files and categories
    signal_files = [
        "wzp6_ee_nuenueH_Hbb_ecm365.root",
        "wzp6_ee_numunumuH_Hbb_ecm365_vbf.root"
    ]

    background_files = [
        "p8_ee_ZZ_ecm365.root",
        "p8_ee_WW_ecm365.root",
        "p8_ee_tt_ecm365.root",
        "wzp6_ee_numunumuH_Hbb_ecm365.root"
    ]

    # Histogram names (as given)
    hist_name = "jj_m"  # Using jj_m (invariant mass of jets) as the observable

    # Load histograms
    signal_hist = load_histograms(signal_files, hist_name)
    background_hist = load_histograms(background_files, hist_name)

    if not signal_hist or not background_hist:
        print("Error: Failed to load histograms.")
        return

    # Define the observable (e.g., m_recoil)
    m_recoil = ROOT.RooRealVar("m_recoil", "Recoil Mass", 120, 140)

    # Convert histograms to RooDataHist
    signal_data = ROOT.RooDataHist("signal_data", "Signal Data", ROOT.RooArgList(m_recoil), signal_hist)
    background_data = ROOT.RooDataHist("background_data", "Background Data", ROOT.RooArgList(m_recoil), background_hist)

    # Define models
    signal_model = define_dscb_model(m_recoil)
    background_model = define_polynomial_model(m_recoil)

    # Combine signal and background models
    nsig = ROOT.RooRealVar("nsig", "Number of Signal Events", signal_hist.Integral(), 0, 1e6)
    nbkg = ROOT.RooRealVar("nbkg", "Number of Background Events", background_hist.Integral(), 0, 1e6)

    model = ROOT.RooAddPdf("model", "Signal + Background Model", ROOT.RooArgList(signal_model, background_model), ROOT.RooArgList(nsig, nbkg))

    # Perform the fit
    result = model.fitTo(signal_data, ROOT.RooFit.Save())

    # Plot the results
    canvas = ROOT.TCanvas("canvas", "Fit Results", 800, 600)
    frame = m_recoil.frame()

    signal_data.plotOn(frame)
    model.plotOn(frame)
    model.plotOn(frame, ROOT.RooFit.Components("background"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))
    model.plotOn(frame, ROOT.RooFit.Components("dscb"), ROOT.RooFit.LineStyle(ROOT.kDotted), ROOT.RooFit.LineColor(ROOT.kBlue))

    frame.Draw()
    output_pdf = os.path.join(outdir, "fit_results.pdf")
    canvas.SaveAs(output_pdf)
    print(f"Fit results saved to {output_pdf}")

    # Print fit results
    result.Print()

if __name__ == "__main__":
    main()

