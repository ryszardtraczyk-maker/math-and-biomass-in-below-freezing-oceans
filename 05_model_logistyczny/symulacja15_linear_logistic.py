# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 22:58:56 2026

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as mticker
import matplotlib
matplotlib.use("Qt5Agg")
import sys
import os

def resource_path(relative_path):
    """Zwraca ścieżkę do pliku zarówno w trybie skryptu, jak i w spakowanym EXE (PyInstaller)."""
    if getattr(sys, "frozen", False):
        # katalog tymczasowy, do którego PyInstaller rozpakowuje zasoby przy --onefile
        base_path = sys._MEIPASS
    else:
        # podczas uruchamiania jako skrypt
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def ask_param(name, default, desc_pl, desc_en):
    print("\n----------------------------------------")
    print(f"PARAMETR: {name}")
    print("Opis (PL):")
    print(desc_pl)
    print("\nDescription (EN):")
    print(desc_en)
    txt = input(f"Wprowadź wartość [{default}]: ")
    return float(txt) if txt.strip() != "" else default


# --- OPISY PARAMETRÓW PL + EN ---

desc_J_chem_pl = """
J_chem – dopływ energii chemicznej dla bakterii.
Im większy, tym szybciej rosną bakterie → rosną korale → rosną ryby.
Zakres stabilny: 0.5 – 3.0
"""
desc_J_chem_en = """
J_chem – chemical energy input for bacteria.
Higher value = faster bacterial growth → more corals → more fish.
Stable range: 0.5 – 3.0
"""

desc_alpha_pl = """
alpha – efektywność przetwarzania energii chemicznej przez bakterie.
Wyższa wartość = szybszy wzrost bakterii.
Zakres: 0.3 – 1.0
"""
desc_alpha_en = """
alpha – efficiency of chemical energy conversion by bacteria.
Higher value = faster bacterial growth.
Range: 0.3 – 1.0
"""

desc_beta_pl = """
beta – naturalna śmiertelność bakterii.
Wyższa wartość = bakterie szybciej zanikają.
Zakres: 0.1 – 0.4
"""
desc_beta_en = """
beta – natural mortality of bacteria.
Higher value = bacteria decline faster.
Range: 0.1 – 0.4
"""

desc_k_BF_pl = """
k_BF – siła zjadania bakterii przez korale.
Wyższa wartość = korale rosną szybciej, bakterie spadają szybciej.
Zakres: 0.05 – 0.15
"""
desc_k_BF_en = """
k_BF – strength of bacterial consumption by corals.
Higher value = faster coral growth, faster bacterial decline.
Range: 0.05 – 0.15
"""

desc_eta_BF_pl = """
eta_BF – efektywność wzrostu korali z bakterii.
Wyższa wartość = korale szybciej rosną.
Zakres: 0.3 – 0.8
"""
desc_eta_BF_en = """
eta_BF – efficiency of coral growth from bacteria.
Higher value = faster coral growth.
Range: 0.3 – 0.8
"""

desc_delta_F_pl = """
delta_F – śmiertelność korali.
Wyższa wartość = korale szybciej zanikają.
Zakres: 0.01 – 0.05
"""
desc_delta_F_en = """
delta_F – coral mortality.
Higher value = faster coral decline.
Range: 0.01 – 0.05
"""

desc_gamma_FP_pl = """
gamma_FP – siła zjadania korali przez ryby.
Wyższa wartość = ryby rosną szybciej, korale spadają szybciej.
Zakres: 0.01 – 0.05
"""
desc_gamma_FP_en = """
gamma_FP – strength of coral consumption by fish.
Higher value = faster fish growth, faster coral decline.
Range: 0.01 – 0.05
"""

desc_eta_FP_pl = """
eta_FP – efektywność wzrostu ryb z korali.
Wyższa wartość = ryby szybciej rosną.
Zakres: 0.2 – 0.6
"""
desc_eta_FP_en = """
eta_FP – efficiency of fish growth from corals.
Higher value = faster fish growth.
Range: 0.2 – 0.6
"""

desc_delta_P_pl = """
delta_P – śmiertelność ryb.
Wyższa wartość = ryby szybciej zanikają.
Zakres: 0.005 – 0.02
"""
desc_delta_P_en = """
delta_P – fish mortality.
Higher value = faster fish decline.
Range: 0.005 – 0.02
"""

desc_r_A_pl = """
r_A – tempo wzrostu alg (produkcja pierwotna).
Wyższa wartość = więcej alg → więcej kryla → więcej ryb.
Zakres: 0.05 – 0.2
"""
desc_r_A_en = """
r_A – algae growth rate (primary production).
Higher value = more algae → more krill → more fish.
Range: 0.05 – 0.2
"""

desc_g_KA_pl = """
g_KA – siła zjadania alg przez kryl.
Wyższa wartość = kryl rośnie szybciej, algi spadają szybciej.
Zakres: 0.01 – 0.05
"""
desc_g_KA_en = """
g_KA – strength of algae consumption by krill.
Higher value = faster krill growth, faster algae decline.
Range: 0.01 – 0.05
"""

desc_m_A_pl = """
m_A – śmiertelność alg.
Wyższa wartość = algi szybciej zanikają.
Zakres: 0.005 – 0.03
"""
desc_m_A_en = """
m_A – algae mortality.
Higher value = faster algae decline.
Range: 0.005 – 0.03
"""

desc_e_KA_pl = """
e_KA – efektywność wzrostu kryla z alg.
Wyższa wartość = kryl szybciej rośnie.
Zakres: 0.3 – 0.6
"""
desc_e_KA_en = """
e_KA – efficiency of krill growth from algae.
Higher value = faster krill growth.
Range: 0.3 – 0.6
"""

desc_m_K_pl = """
m_K – śmiertelność kryla.
Wyższa wartość = kryl szybciej zaniknie.
Zakres: 0.01 – 0.05
"""
desc_m_K_en = """
m_K – krill mortality.
Higher value = faster krill decline.
Range: 0.01 – 0.05
"""

desc_g_PK_pl = """
g_PK – siła zjadania kryla przez ryby.
Wyższa wartość = ryby rosną szybciej, kryl spada szybciej.
Zakres: 0.01 – 0.05
"""
desc_g_PK_en = """
g_PK – strength of krill consumption by fish.
Higher value = faster fish growth, faster krill decline.
Range: 0.01 – 0.05
"""


# --- WPROWADZANIE PARAMETRÓW ZIEMI ---
print("\n=== Parametry Ziemi ===")

J_chem_earth = ask_param("Ziemia: J_chem", 1.5, desc_J_chem_pl, desc_J_chem_en)
alpha_earth  = ask_param("Ziemia: alpha", 0.6, desc_alpha_pl, desc_alpha_en)
beta_earth   = ask_param("Ziemia: beta", 0.25, desc_beta_pl, desc_beta_en)
k_BF_earth   = ask_param("Ziemia: k_BF", 0.08, desc_k_BF_pl, desc_k_BF_en)
eta_BF_earth = ask_param("Ziemia: eta_BF", 0.6, desc_eta_BF_pl, desc_eta_BF_en)
delta_F_earth = ask_param("Ziemia: delta_F", 0.03, desc_delta_F_pl, desc_delta_F_en)
gamma_FP_earth = ask_param("Ziemia: gamma_FP", 0.02, desc_gamma_FP_pl, desc_gamma_FP_en)
eta_FP_earth   = ask_param("Ziemia: eta_FP", 0.4, desc_eta_FP_pl, desc_eta_FP_en)
delta_P_earth  = ask_param("Ziemia: delta_P", 0.009, desc_delta_P_pl, desc_delta_P_en)
r_A_earth  = ask_param("Ziemia: r_A", 0.16, desc_r_A_pl, desc_r_A_en)
g_KA_earth = ask_param("Ziemia: g_KA", 0.014, desc_g_KA_pl, desc_g_KA_en)
m_A_earth  = ask_param("Ziemia: m_A", 0.009, desc_m_A_pl, desc_m_A_en)
e_KA_earth = ask_param("Ziemia: e_KA", 0.62, desc_e_KA_pl, desc_e_KA_en)
m_K_earth  = ask_param("Ziemia: m_K", 0.005, desc_m_K_pl, desc_m_K_en)
g_PK_earth = ask_param("Ziemia: g_PK", 0.012, desc_g_PK_pl, desc_g_PK_en)


# --- WPROWADZANIE PARAMETRÓW EUROPY ---
print("\n=== Parametry Europy ===")

J_chem_moon = ask_param("Europa: J_chem", 1.8, desc_J_chem_pl, desc_J_chem_en)
alpha_moon  = ask_param("Europa: alpha", 0.7, desc_alpha_pl, desc_alpha_en)
beta_moon   = ask_param("Europa: beta", 0.25, desc_beta_pl, desc_beta_en)
k_BF_moon   = ask_param("Europa: k_BF", 0.09, desc_k_BF_pl, desc_k_BF_en)
eta_BF_moon = ask_param("Europa: eta_BF", 0.6, desc_eta_BF_pl, desc_eta_BF_en)
delta_F_moon = ask_param("Europa: delta_F", 0.03, desc_delta_F_pl, desc_delta_F_en)
gamma_FP_moon = ask_param("Europa: gamma_FP", 0.02, desc_gamma_FP_pl, desc_gamma_FP_en)
eta_FP_moon   = ask_param("Europa: eta_FP", 0.4, desc_eta_FP_pl, desc_eta_FP_en)
delta_P_moon  = ask_param("Europa: delta_P", 0.007, desc_delta_P_pl, desc_delta_P_en)
r_A_moon  = ask_param("Europa: r_A", 0.11, desc_r_A_pl, desc_r_A_en)
g_KA_moon = ask_param("Europa: g_KA", 0.025, desc_g_KA_pl, desc_g_KA_en)
m_A_moon  = ask_param("Europa: m_A", 0.01, desc_m_A_pl, desc_m_A_en)
e_KA_moon = ask_param("Europa: e_KA", 0.45, desc_e_KA_pl, desc_e_KA_en)
m_K_moon  = ask_param("Europa: m_K", 0.02, desc_m_K_pl, desc_m_K_en)
g_PK_moon = ask_param("Europa: g_PK", 0.035, desc_g_PK_pl, desc_g_PK_en)


# ---------- ODE: B, F, P (icefish = Pg+Ca+Cg), A (ice algae), K (krill) ----------

def integrate_ode(t, dt, X0, params, v_curr_series, is_earth=True):
    B0, F0, P0, A0, K0 = X0

    (J_chem, alpha, beta, k_BF, eta_BF, delta_F,
     gamma_FP, eta_FP, delta_P,
     r_A, g_KA, m_A,
     e_KA, m_K,
     g_PK) = params

    N = len(t)
    X = np.zeros((N, 5))
    X[0, :] = [B0, F0, P0, A0, K0]

    def dXdt(ti, Xi, vc):
        B, F, P, A, K = Xi

        # --- B-F-P ---
        gamma_BF_t = k_BF * vc
        dB = alpha * J_chem - beta * B - gamma_BF_t * B * F
        dF = eta_BF * gamma_BF_t * B * F - delta_F * F - gamma_FP * F * P
        dP = eta_FP * gamma_FP * F * P - delta_P * P

        # --- A: ice algae + okrzemki + roztopy ---
        if is_earth:
            J_A = 0.005 * (1 + 0.3 * np.sin(2*np.pi*ti/365.0))
        else:
            J_A = 0.008 * (1 + 0.2 * np.sin(2*np.pi*ti/500.0))

        dA = r_A * A - g_KA * K * A - m_A * A + J_A

        # --- K: krill (z dopływem z prądu antarktycznego / podlodowego) ---
        G_PK = g_PK * P * K
        if is_earth:
            J_K = 0.003 * (1 + 0.3 * np.sin(2*np.pi*ti/365.0))
        else:
            J_K = 0.004

        dK = e_KA * g_KA * K * A - m_K * K - G_PK + J_K

        # sprzężenie zwrotne: krill wzmacnia drapieżnika (łagodniej)
        dP += 0.02 * G_PK

        return np.array([dB, dF, dP, dA, dK])

    for i in range(N - 1):
        ti = t[i]
        Xi = X[i, :]
        vc = v_curr_series[i]

        k1 = dXdt(ti, Xi, vc)
        k2 = dXdt(ti + dt/2, Xi + dt*k1/2, vc)
        k3 = dXdt(ti + dt/2, Xi + dt*k2/2, vc)
        k4 = dXdt(ti + dt, Xi + dt*k3, vc)

        X[i+1, :] = Xi + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

    return X

# ---------- czas ----------

t0, t_end = 0.0, 1500.0
dt = 1.0
N = int((t_end - t0) / dt) + 1
t = np.linspace(t0, t_end, N)

# ---------- wartości początkowe (minima CCAMLR, znormalizowane) ----------

B0, F0, P0 = 0.3, 0.2, 0.03   # bakterie, fitoplankton, icefish
A0, K0 = 0.4, 0.2             # algi lodowe + okrzemki, kryl

# ---------- Ziemia: parametry ----------

params_earth = [
    J_chem_earth, alpha_earth, beta_earth,
    k_BF_earth, eta_BF_earth, delta_F_earth,
    gamma_FP_earth, eta_FP_earth, delta_P_earth,
    r_A_earth, g_KA_earth, m_A_earth,
    e_KA_earth, m_K_earth,
    g_PK_earth
]

v_curr_mean_earth = 0.18
v_curr_earth = v_curr_mean_earth * (1 + 0.3*np.sin(2*np.pi*t/365))

climate_e = np.sin(2*np.pi*t/365*4)  # 4-letni cykl zimne/ciepłe

X_earth = integrate_ode(t, dt, [B0, F0, P0, A0, K0], params_earth, v_curr_earth, is_earth=True)
B_e, F_e, P_e, A_e, K_e = X_earth.T

climate_e = np.sin(2*np.pi*t/365*4)

# P. georgianus – bardziej w zimnych latach (lód)
Pg_e = (0.45 + 0.10*climate_e) * P_e

# C. aceratus – w opozycji do Pg (więcej w cieplejszych, bez lodu)
Ca_e = (0.50 - 0.10*climate_e) * P_e

# C. gunnari – mniej zależny od klimatu, bardziej od kryla
Cg_e = (1.50 + 0.05*(K_e / (K_e.max() + 1e-6))) * P_e

icefish_e = Pg_e + Ca_e + Cg_e

# ---------- Europa: parametry (z ask_param, bez nadpisywania) ----------

params_moon = [
    J_chem_moon, alpha_moon, beta_moon,
    k_BF_moon, eta_BF_moon, delta_F_moon,
    gamma_FP_moon, eta_FP_moon, delta_P_moon,
    r_A_moon, g_KA_moon, m_A_moon,
    e_KA_moon, m_K_moon,
    g_PK_moon
]

v_curr_mean_moon = 0.22
v_curr_moon = v_curr_mean_moon * (1 + 0.1*np.sin(2*np.pi*t/500))

X_moon = integrate_ode(t, dt, [B0, F0, P0, A0, K0], params_moon, v_curr_moon, is_earth=False)
B_m, F_m, P_m, A_m, K_m = X_moon.T

Pg_m = 0.45 * P_m
Ca_m = 0.50 * P_m
Cg_m = 1.50 * P_m
icefish_m = Pg_m + Ca_m + Cg_m  # ~2.45 * P_m

# ---------- Animacja: dwa wykresy (Earth / Europa, podwójne osie Y) ----------

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=False)

# ============================
# EARTH PANEL
# ============================

line_B_e, = ax1.plot([], [], linestyle=':', color='gray', linewidth=2)
line_F_e, = ax1.plot([], [], linestyle='-', color='lightskyblue', linewidth=2)
line_P_e, = ax1.plot([], [], linestyle='-', color='black', linewidth=2)

ax1_right = ax1.twinx()
line_A_e, = ax1_right.plot([], [], linestyle='--', color='green', linewidth=3)
line_K_e, = ax1_right.plot([], [], linestyle='-', color='red', linewidth=3)

ax1.text(0.02, 1.0, "Earth Under Ice Antarctic freeze life",
         transform=ax1.transAxes, fontsize=11, ha='left', va='top')

ax1.set_xlim(t0, t_end)

xticks = np.arange(0, t_end + 1, 100)
ax1.set_xticks(xticks)

def format_hundreds(x, pos):
    return f"{int(x/100)}"

ax1.xaxis.set_major_formatter(mticker.FuncFormatter(format_hundreds))

ax1.set_xlabel("Time [⋅10² days]", loc='left')

for spine in ax1.spines.values():
    spine.set_visible(False)
for spine in ax1_right.spines.values():
    spine.set_visible(False)

ax1.tick_params(axis='y', length=4)
ax1_right.tick_params(axis='y', length=4)

ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))
ax1_right.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))

ax1.set_yticks(
    np.linspace(
        0,
        int(max(B_e.max(), F_e.max(), P_e.max()) * 1.2),
        6
    )
)
ax1_right.set_yticks(
    np.linspace(
        0,
        int(max(A_e.max(), K_e.max()) * 1.2),
        6
    )
)

ax1.set_ylabel(
    r"$Biomass_{\mathrm{normalized}}ᴮᵃᶜᵗᵉʳⁱᵉˢᴗᶜᵒˡᵈ ᶜᵒʳᵃˡˢᴗ³ᴵᶜᵉᶠⁱˢʰ$ "
    r"($B³ᴵᶜᵉᶠⁱˢʰₙₒᵣₘ[⋅2.45t⋅km⁻²] \mathrm{ } \approx  [⋅1934ind⋅km⁻²]$)",
    loc='top'
)

from matplotlib.offsetbox import OffsetImage, AnnotationBbox

ax1.add_artist(AnnotationBbox(OffsetImage(plt.imread(resource_path("p_georgianus.png")), zoom=0.25),
                              (0.90, 0.07), xycoords='axes fraction', frameon=False))
ax1.text(0.85, 0.06, "\n55 cm TL\n1795 g",
         ha='center', va='top', fontsize=8, transform=ax1.transAxes)
ax1.text(0.70, 0.03, "██████", color='black', fontsize=9, fontweight='bold', transform=ax1.transAxes)

ax1.add_artist(AnnotationBbox(OffsetImage(plt.imread(resource_path("l_pertusa.png")), zoom=0.0625),
                              (0.90, 0.30), xycoords='axes fraction', frameon=False))
ax1.text(0.92, 0.25,
         "\n15 cm colony\n1000 g\n~300 polyps",
         ha='center', va='top', fontsize=8, transform=ax1.transAxes)
ax1.text(0.78, 0.19, "██████", color='lightskyblue', fontsize=9, fontweight='bold', transform=ax1.transAxes)

ax1.add_artist(AnnotationBbox(OffsetImage(plt.imread(resource_path("kryl2.png")), zoom=0.125),
                              (0.90, 0.60), xycoords='axes fraction', frameon=False))
ax1.text(0.95, 0.59, "\n6 cm\n1.72 g",
         ha='center', va='top', fontsize=8, transform=ax1.transAxes)
ax1.text(0.80, 0.54, "██████", color='red', fontsize=9, fontweight='bold', transform=ax1.transAxes)

ax1.add_artist(AnnotationBbox(OffsetImage(plt.imread(resource_path("beggiatoa.png")), zoom=0.125),
                              (0.90, 0.92), xycoords='axes fraction', frameon=False))
ax1.text(0.92, 0.93, "\n10 µm\n1⋅10⁻¹² kg",
         ha='center', va='top', fontsize=8, transform=ax1.transAxes)
ax1.text(0.78, 0.88, "••••••", color='gray', fontsize=9, fontweight='bold', transform=ax1.transAxes)

ax1.add_artist(AnnotationBbox(OffsetImage(plt.imread(resource_path("iceAlgae.png")), zoom=0.125),
                              (0.90, 0.79), xycoords='axes fraction', frameon=False))
ax1.text(0.95, 0.76, "\n2-2000 µm\n10-100 C ng⋅cell⁻¹",
         ha='center', va='top', fontsize=8, transform=ax1.transAxes)
ax1.text(0.78, 0.73, "▬▬▬▬▬", color='green', fontsize=9, fontweight='bold', transform=ax1.transAxes)


# ============================
# EUROPA PANEL
# ============================

line_B_m, = ax2.plot([], [], linestyle=':', color='gray', linewidth=2)
line_F_m, = ax2.plot([], [], linestyle='-', color='lightskyblue', linewidth=2)
line_P_m, = ax2.plot([], [], linestyle='-', color='black', linewidth=2)

ax2_right = ax2.twinx()
line_A_m, = ax2_right.plot([], [], linestyle='--', color='green', linewidth=3)
line_K_m, = ax2_right.plot([], [], linestyle='-', color='red', linewidth=3)

ax2.text(0.02, 1.0, "Jupiter's Europe Icy cave life",
         transform=ax2.transAxes, fontsize=11, ha='left', va='top')

ax2.set_xlim(t0, t_end)
xticks2 = np.arange(0, t_end + 1, 100)
ax2.set_xticks(xticks2)

ax2.xaxis.set_major_formatter(mticker.FuncFormatter(format_hundreds))

for spine in ax2.spines.values():
    spine.set_visible(False)
for spine in ax2_right.spines.values():
    spine.set_visible(False)

ax2.tick_params(axis='y', length=4)
ax2_right.tick_params(axis='y', length=4)

ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))
ax2_right.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))

ax2.set_yticks(
    np.linspace(
        0,
        int(max(B_m.max(), F_m.max(), P_m.max()) * 1.2),
        6
    )
)
ax2_right.set_yticks(
    np.linspace(
        0,
        int(max(A_m.max(), K_m.max()) * 1.2),
        6
    )
)

ax2_right.set_ylabel(
    r"$Biomass_{\mathrm{normalized}} ᴵᶜᵉᴬˡᵍᵃᵉ\mathrm{ᴗ} ᴷʳⁱˡˡ$ "
    r"($Bᴷʳⁱˡˡₙₒᵣₘ[⋅40t⋅km⁻²] \mathrm{ } \approx  [⋅3.41⋅10⁷ind⋅km⁻²]$)",
    loc='top'
)

plt.tight_layout()

fig.text(0.13, 0.03, "Bᴮᵃᶜᵗᵉʳⁱᵉˢₙₒᵣₘ••••••[⋅0.03t⋅km⁻²]", color='gray', fontsize=9, fontweight='bold')
fig.text(0.13 + 0.16, 0.03, "Bᴵᶜᵉᴬˡᵍᵃᵉₙₒᵣₘ▬▬▬▬▬[⋅37t⋅km⁻²]", color='green', fontsize=9, fontweight='bold')
fig.text(0.13 + 0.32, 0.03, "Bᴷʳⁱˡˡₙₒᵣₘ██████[⋅40t⋅km⁻²]", color='red', fontsize=9, fontweight='bold')
fig.text(0.14 + 0.45, 0.03, "Bᶜᵒˡᵈ ᶜᵒʳᵃˡˢₙₒᵣₘ██████[⋅0.16t⋅km⁻²]", color='lightskyblue', fontsize=9, fontweight='bold')
fig.text(0.13 + 0.64, 0.03, "B³ᴵᶜᵉᶠⁱˢʰₙₒᵣₘ██████[⋅(0.45+0.5+1.5)t⋅km⁻²]", color='black', fontsize=9, fontweight='bold')

def update(frame):
    ts = t[:frame]

    line_B_e.set_data(ts, B_e[:frame])
    line_F_e.set_data(ts, F_e[:frame])
    line_P_e.set_data(ts, P_e[:frame])
    line_A_e.set_data(ts, A_e[:frame])
    line_K_e.set_data(ts, K_e[:frame])

    line_B_m.set_data(ts, B_m[:frame])
    line_F_m.set_data(ts, F_m[:frame])
    line_P_m.set_data(ts, P_m[:frame])
    line_A_m.set_data(ts, A_m[:frame])
    line_K_m.set_data(ts, K_m[:frame])

    return (
        line_B_e, line_F_e, line_P_e, line_A_e, line_K_e,
        line_B_m, line_F_m, line_P_m, line_A_m, line_K_m
    )

anim = FuncAnimation(fig, update, frames=N, interval=20, blit=True)

plt.show()

save_gif = input("Zapisać animację do GIF? (t/n): ").lower()

if save_gif == "t":
    import datetime
    import time
    import sys
    import threading

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"animacja_biomasy_{timestamp}.gif"

    print(f"Zapisuję GIF jako: {filename}")
    print("Postęp zapisu (gwiazdka = minęła 1 minuta): ", end="")
    sys.stdout.flush()

    running = True

    def star_thread():
        last_minute = datetime.datetime.now().minute
        while running:
            now_minute = datetime.datetime.now().minute
            if now_minute != last_minute:
                print("*", end="")
                sys.stdout.flush()
                last_minute = now_minute
            time.sleep(1)

    star_thread_obj = threading.Thread(target=star_thread)
    star_thread_obj.start()

    try:
        anim.save(filename, writer="pillow", fps=20)
    except Exception as e:
        print("\nBłąd podczas zapisu GIF:", e)

    running = False
    star_thread_obj.join()

    print("\nZapis zakończony.")

save_mp4 = input("Zapisać animację do MP4? (t/n): ").lower()

if save_mp4 == "t":
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_mp4 = f"animacja_biomasy_{timestamp}.mp4"

    print(f"Zapisuję MP4 jako: {filename_mp4}")

    try:
        anim.save(filename_mp4, writer="ffmpeg", fps=20)
        print("Plik MP4 zapisany.")
    except Exception as e:
        print("Błąd podczas zapisu MP4:", e)

save_params = input("Zapisać parametry do pliku TXT? (t/n): ").lower()

if save_params == "t":
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"parametry_{timestamp}.txt"

    with open(fname, "w") as f:
        f.write("=== Parametry Ziemi ===\n")
        f.write(f"J_chem = {J_chem_earth}\n")
        f.write(f"alpha = {alpha_earth}\n")
        f.write(f"beta = {beta_earth}\n")
        f.write(f"k_BF = {k_BF_earth}\n")
        f.write(f"eta_BF = {eta_BF_earth}\n")
        f.write(f"delta_F = {delta_F_earth}\n")
        f.write(f"gamma_FP = {gamma_FP_earth}\n")
        f.write(f"eta_FP = {eta_FP_earth}\n")
        f.write(f"delta_P = {delta_P_earth}\n")
        f.write(f"r_A = {r_A_earth}\n")
        f.write(f"g_KA = {g_KA_earth}\n")
        f.write(f"m_A = {m_A_earth}\n")
        f.write(f"e_KA = {e_KA_earth}\n")
        f.write(f"m_K = {m_K_earth}\n")
        f.write(f"g_PK = {g_PK_earth}\n")

        f.write("\n=== Parametry Europy ===\n")
        f.write(f"J_chem = {J_chem_moon}\n")
        f.write(f"alpha = {alpha_moon}\n")
        f.write(f"beta = {beta_moon}\n")
        f.write(f"k_BF = {k_BF_moon}\n")
        f.write(f"eta_BF = {eta_BF_moon}\n")
        f.write(f"delta_F = {delta_F_moon}\n")
        f.write(f"gamma_FP = {gamma_FP_moon}\n")
        f.write(f"eta_FP = {eta_FP_moon}\n")
        f.write(f"delta_P = {delta_P_moon}\n")
        f.write(f"r_A = {r_A_moon}\n")
        f.write(f"g_KA = {g_KA_moon}\n")
        f.write(f"m_A = {m_A_moon}\n")
        f.write(f"e_KA = {e_KA_moon}\n")
        f.write(f"m_K = {m_K_moon}\n")
        f.write(f"g_PK = {g_PK_moon}\n")

    print(f"Parametry zapisane do pliku: {fname}")

save_xlsx = input("Zapisać wszystkie przebiegi do jednego pliku XLSX? (t/n): ").lower()

if save_xlsx == "t":
    import datetime
    import pandas as pd

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    xlsx_name = f"wszystko_{timestamp}.xlsx"

    print(f"Zapisuję wszystkie przebiegi do pliku: {xlsx_name}")

    df = pd.DataFrame({
        "czas": t,
        "B_e": X_earth[:, 0],
        "F_e": X_earth[:, 1],
        "P_e": X_earth[:, 2],
        "A_e": X_earth[:, 3],
        "K_e": X_earth[:, 4],
        "B_m": X_moon[:, 0],
        "F_m": X_moon[:, 1],
        "P_m": X_moon[:, 2],
        "A_m": X_moon[:, 3],
        "K_m": X_moon[:, 4],
        "ΔB": X_moon[:, 0] - X_earth[:, 0],
        "ΔF": X_moon[:, 1] - X_earth[:, 1],
        "ΔP": X_moon[:, 2] - X_earth[:, 2],
        "ΔA": X_moon[:, 3] - X_earth[:, 3],
        "ΔK": X_moon[:, 4] - X_earth[:, 4],
        "Pg_e": Pg_e,
        "Ca_e": Ca_e,
        "Cg_e": Cg_e,
        "Pg_m": Pg_m,
        "Ca_m": Ca_m,
        "Cg_m": Cg_m,
        "climate_e": climate_e,
        "v_curr_earth": v_curr_earth,
        "v_curr_moon": v_curr_moon
    })

    df.to_excel(xlsx_name, index=False)
    print("Plik XLSX zapisany.")

save_csv_all = input("Zapisać wszystkie przebiegi do jednego pliku CSV? (t/n): ").lower()

if save_csv_all == "t":
    import datetime, csv
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_name = f"wszystko_{timestamp}.csv"

    print(f"Zapisuję wszystkie przebiegi do pliku: {csv_name}")

    with open(csv_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "czas",
            "B_e", "F_e", "P_e", "A_e", "K_e",
            "B_m", "F_m", "P_m", "A_m", "K_m",
            "dB", "dF", "dP", "dA", "dK",
            "Pg_e", "Ca_e", "Cg_e",
            "Pg_m", "Ca_m", "Cg_m",
            "climate_e",
            "v_curr_earth", "v_curr_moon"
        ])

        for i in range(len(t)):
            writer.writerow([
                t[i],
                X_earth[i, 0], X_earth[i, 1], X_earth[i, 2], X_earth[i, 3], X_earth[i, 4],
                X_moon[i, 0], X_moon[i, 1], X_moon[i, 2], X_moon[i, 3], X_moon[i, 4],
                X_moon[i, 0] - X_earth[i, 0],
                X_moon[i, 1] - X_earth[i, 1],
                X_moon[i, 2] - X_earth[i, 2],
                X_moon[i, 3] - X_earth[i, 3],
                X_moon[i, 4] - X_earth[i, 4],
                Pg_e[i], Ca_e[i], Cg_e[i],
                Pg_m[i], Ca_m[i], Cg_m[i],
                climate_e[i],
                v_curr_earth[i], v_curr_moon[i]
            ])

    print("Plik CSV zapisany.")


print("Program zakończony.")
os._exit(0)
