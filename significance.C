#include <iostream>
#include <vector>
#include <string>
#include <TFile.h>
#include <TH1F.h>
#include <cmath> 

int sigma() {
    std::vector<std::string> signal_procs = {
        "wzp6_ee_nuenueH_Hbb_ecm365",
        "wzp6_ee_numunumuH_Hbb_ecm365_vbf"
    };

    std::vector<std::string> background_procs = {
        "p8_ee_ZZ_ecm365",
        "p8_ee_WW_ecm365",
        "p8_ee_tt_ecm365",
        "wzp6_ee_numunumuH_Hbb_ecm365"
    };

    std::string hist_name = "jj_m";

    double total_signal = 0.0;
    double total_background = 0.0;

    std::cout << "Procesando histogramas de señal..." << std::endl;
    for (const auto& proc : signal_procs) {
        std::string filename = proc + ".root"; 
        TFile *file = TFile::Open(filename.c_str());

        if (!file || file->IsZombie()) {
            std::cerr << "Error: No se pudo abrir el archivo " << filename << std::endl;
            continue;
        }

        TH1F *hist = (TH1F*)file->Get(hist_name.c_str());
        if (!hist) {
            std::cerr << "Advertencia: No se encontró el histograma " << hist_name
                      << " en el archivo '" << filename << "'." << std::endl;
            file->Close();
            continue;
        }

        double integral = hist->Integral();
        total_signal += integral;
        std::cout << "Integral del histograma " << hist_name
                  << " en el proceso " << proc << ": " << integral << std::endl;

        file->Close();
    }

    std::cout << "\nProcesando Background..." << std::endl;
    for (const auto& proc : background_procs) {
        std::string filename = proc + ".root"; 
        TFile *file = TFile::Open(filename.c_str());

        if (!file || file->IsZombie()) {
            std::cerr << "Error: No se pudo abrir el archivo " << filename << std::endl;
            continue;
        }

        TH1F *hist = (TH1F*)file->Get(hist_name.c_str());
        if (!hist) {
            std::cerr << "Advertencia: No se encontró el histograma " << hist_name
                      << " en el archivo '" << filename << "'." << std::endl;
            file->Close();
            continue;
        }

        double integral = hist->Integral();
        total_background += integral;
        std::cout << "Integral del histograma " << hist_name
                  << " en el proceso " << proc << ": " << integral << std::endl;

        file->Close();
    }

    // Significancia con fluctuaciones de fondo
    std::cout << "\nResultados finales:" << std::endl;
    std::cout << "Total señal: " << total_signal << std::endl;
    std::cout << "Total fondo: " << total_background << std::endl;

    if (total_background > 0) {
        // Fluctuaciones de fondo: raíz cuadrada de la integral del fondo
        double background_fluctuation = sqrt(total_background);

        // Significancia considerando fluctuaciones
        double significance = total_signal / sqrt(total_background + background_fluctuation * background_fluctuation);
        std::cout << "Significancia (con fluctuaciones de fondo): " << significance << std::endl;
    } else {
        std::cerr << "Error: El fondo es cero, no se puede calcular la significancia." << std::endl;
    }

    return 0;
}
