#ifndef HIGGS_ANALYSIS_H
#define HIGGS_ANALYSIS_H

#include <cmath>
#include <vector>
#include <algorithm>
#include <iostream>

#include "TLorentzVector.h"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "ReconstructedParticle2MC.h"

namespace FCCAnalyses { namespace HiggsAnalysis {

using Vec_rp = std::vector<edm4hep::ReconstructedParticleData>;
using Vec_i = std::vector<int>;
using Vec_mc = std::vector<edm4hep::MCParticleData>;

// build the Higgs resonance based on the available b-jets. Returns the best b-jet pair compatible with the Higgs mass and the recoil.
struct HiggsResonanceBuilder {
    float m_higgs_mass;
    float ecm;
    bool m_use_MC_Kinematics;
    float chi2_recoil_frac;

    HiggsResonanceBuilder(float arg_higgs_mass, float arg_ecm, bool use_MC_Kinematics = false, float chi2_frac = 0.5);
    Vec_rp operator()(Vec_rp bjets, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc);
};

HiggsResonanceBuilder::HiggsResonanceBuilder(float arg_higgs_mass, float arg_ecm, bool use_MC_Kinematics, float chi2_frac)
    : m_higgs_mass(arg_higgs_mass), ecm(arg_ecm), m_use_MC_Kinematics(use_MC_Kinematics), chi2_recoil_frac(chi2_frac) {}

Vec_rp HiggsResonanceBuilder::operator()(Vec_rp bjets, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc) {
    Vec_rp result;
    result.reserve(2);

    std::vector<std::vector<int>> pairs;
    int n = bjets.size();
  
    if (n > 1) {
        std::vector<bool> v(n);
        std::fill(v.end() - 2, v.end(), true);
        do {
            std::vector<int> pair;
            edm4hep::ReconstructedParticleData reso;
            TLorentzVector reso_lv;
            for (int i = 0; i < n; ++i) {
                if (v[i]) {
                    pair.push_back(i);
                    TLorentzVector jet_lv;

                    if (m_use_MC_Kinematics) {
                        int track_index = bjets[i].tracks_begin;
                        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
                        if (mc_index >= 0 && mc_index < mc.size()) {
                            jet_lv.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
                        }
                    } else {
                        jet_lv.SetXYZM(bjets[i].momentum.x, bjets[i].momentum.y, bjets[i].momentum.z, bjets[i].mass);
                    }

                    reso_lv += jet_lv;
                }
            }

            reso.momentum.x = reso_lv.Px();
            reso.momentum.y = reso_lv.Py();
            reso.momentum.z = reso_lv.Pz();
            reso.mass = reso_lv.M();
            result.push_back(reso);
            pairs.push_back(pair);

        } while (std::next_permutation(v.begin(), v.end()));
    } else {
        std::cerr << "ERROR: HiggsResonanceBuilder, at least two b-jets required." << std::endl;
        exit(1);
    }
  
    if (result.size() > 1) {
        Vec_rp bestReso;
        int idx_min = -1;
        float d_min = 9e9;
        for (int i = 0; i < result.size(); ++i) {
            auto recoil_p4 = TLorentzVector(0, 0, 0, ecm);
            TLorentzVector tv1;
            tv1.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
            recoil_p4 -= tv1;
      
            auto recoil_fcc = edm4hep::ReconstructedParticleData();
            recoil_fcc.momentum.x = recoil_p4.Px();
            recoil_fcc.momentum.y = recoil_p4.Py();
            recoil_fcc.momentum.z = recoil_p4.Pz();
            recoil_fcc.mass = recoil_p4.M();
            
            float mass_diff = std::pow(result.at(i).mass - m_higgs_mass, 2);
            float rec_diff = std::pow(recoil_fcc.mass - m_higgs_mass, 2); // Assuming recoil mass similar to Higgs mass for simplification
            float d = (1.0 - chi2_recoil_frac) * mass_diff + chi2_recoil_frac * rec_diff;
            
            if (d < d_min) {
                d_min = d;
                idx_min = i;
            }
        }

        if (idx_min >= 0 && idx_min < result.size()) {
            bestReso.push_back(result.at(idx_min));
            auto &b1 = bjets[pairs[idx_min][0]];
            auto &b2 = bjets[pairs[idx_min][1]];
            bestReso.push_back(b1);
            bestReso.push_back(b2);
        } else {
            std::cerr << "ERROR: HiggsResonanceBuilder, no minimum found." << std::endl;
            exit(1);
        }
        return bestReso;
    } else {
        auto &b1 = bjets[0];
        auto &b2 = bjets[1];
        result.push_back(b1);
        result.push_back(b2);
        return result;
    }
}

struct JetMass {
    Vec_rp operator() (Vec_rp in, float m_jet_mass);
};

Vec_rp JetMass::operator() (Vec_rp in, float m_jet_mass) {
    Vec_rp result;
    result.reserve(in.size());
    for (auto &p : in) {
        if (std::fabs(p.mass - m_jet_mass) < 5.0) {
            result.push_back(p);
        }
    }
    return result;
}

struct DeltaPhi {
    std::vector<float> operator() (Vec_rp in);
};

std::vector<float> DeltaPhi::operator() (Vec_rp in) {
    std::vector<float> result;
    if (in.size() >= 2) {
        TLorentzVector lv1;
        lv1.SetPxPyPzE(in[0].momentum.x, in[0].momentum.y, in[0].momentum.z, in[0].energy);
        TLorentzVector lv2;
        lv2.SetPxPyPzE(in[1].momentum.x, in[1].momentum.y, in[1].momentum.z, in[1].energy);
        double dphi = std::fabs(lv1.Phi() - lv2.Phi());
        if (dphi > M_PI) dphi = 2 * M_PI - dphi;
        result.push_back(dphi);
    }
    return result;
}

} } // namespace FCCAnalyses::HiggsAnalysis

#endif
