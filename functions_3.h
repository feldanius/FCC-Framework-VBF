#ifndef ZHfunctions_H
#define ZHfunctions_H

#include <cmath>
#include <vector>
#include <math.h>
#include <algorithm>  //extra
#include <iostream>   //extra

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"
#include "ReconstructedParticle2MC.h"


namespace FCCAnalyses { namespace ZHfunctions {

// build the Higgs resonance based on the available b-jets. Returns the best b-jet pair compatible with the Higgs mass and the recoil.
struct HiggsResonanceBuilder {
    float m_higgs_mass;
    float m_recoil_mass;
    float chi2_recoil_frac;
    float ecm;
    bool m_use_MC_Kinematics;
    HiggsResonanceBuilder(float arg_higgs_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics);
    Vec_rp operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) ;
};

HiggsResonanceBuilder::HiggsResonanceBuilder(float arg_higgs_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics) {m_higgs_mass = arg_higgs_mass, m_recoil_mass = arg_recoil_mass, chi2_recoil_frac = arg_chi2_recoil_frac, ecm = arg_ecm, m_use_MC_Kinematics = arg_use_MC_Kinematics;}

Vec_rp HiggsResonanceBuilder::HiggsResonanceBuilder::operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) {
  
    Vec_rp result;
    result.reserve(3);
    std::vector<std::vector<int>> pairs; 
    int n = legs.size();
  
    if(n > 1) {
        ROOT::VecOps::RVec<bool> v(n);
        std::fill(v.end() - 2, v.end(), true);
        do {
            std::vector<int> pair;
            rp reso;
            reso.charge = 0;
            TLorentzVector reso_lv;
            for (int i = 0; i < n; ++i) {
                if (v[i]) {
                    pair.push_back(i);
                    reso.charge += legs[i].charge;
                    TLorentzVector leg_lv;

                    if(m_use_MC_Kinematics) { 
                        int track_index = legs[i].tracks_begin;   // index in the Track array
                        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
                        if (mc_index >= 0 && mc_index < mc.size()) {
                            leg_lv.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
                        }
                    }  else { // reco kinematics
                         leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
                    }

                    reso_lv += leg_lv;
                }
            }

            if(reso.charge != 0) continue;
            reso.momentum.x = reso_lv.Px();
            reso.momentum.y = reso_lv.Py();
            reso.momentum.z = reso_lv.Pz();
            reso.mass = reso_lv.M();
            result.emplace_back(reso);
            pairs.push_back(pair);

        } while (std::next_permutation(v.begin(), v.end()));
    } else {
        std::cerr << "ERROR: HiggsResonanceBuilder, at least two two leptons required." << std::endl;
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

            TLorentzVector tg;
            tg.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);

            float boost = tg.P();
            float mass_diff = std::pow(result.at(i).mass - m_higgs_mass, 2);
            float rec_diff = std::pow(recoil_fcc.mass - m_higgs_mass, 2); // Assuming recoil mass similar to Higgs mass for simplification
            float d = (1.0 - chi2_recoil_frac) * mass_diff + chi2_recoil_frac * rec_diff;
            
            if (d < d_min) {
                d_min = d;
                idx_min = i;
            }
        }

        if (idx_min >= 0 && idx_min < result.size()) {   //modification original:  if(idx_min > -1) 
            bestReso.push_back(result.at(idx_min));
            auto & l1 = legs[pairs[idx_min][0]];
            auto & l2 = legs[pairs[idx_min][1]];
            bestReso.emplace_back(l1);
            bestReso.emplace_back(l2);
        } else {
            std::cerr << "ERROR: HiggsResonanceBuilder, no minimum found." << std::endl;
            exit(1);
        }
        return bestReso;
    } else {
        auto & l1 = legs[0];
        auto & l2 = legs[1];
        result.emplace_back(l1);
        result.emplace_back(l2);
        return result;
    }
}

////////////////////////continue here///////////////////////77

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
