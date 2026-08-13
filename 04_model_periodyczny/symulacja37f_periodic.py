# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 14:18:31 2026

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.ticker as mticker
import matplotlib
matplotlib.use("Qt5Agg")
import sys
import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


# ============================
# FUNKCJA DO WPROWADZANIA PARAMETRÓW
# ============================
def ask_param(name, default, desc_pl, desc_en):
    print("\n----------------------------------------")
    print(f"PARAMETR: {name}")
    print("Opis (PL):")
    print(desc_pl)
    print("\nDescription (EN):")
    print(desc_en)
    txt = input(f"Wprowadź wartość [{default}]: ")
    return float(txt) if txt.strip() != "" else default




def resource_path(relative_path):
    """Zwraca ścieżkę do pliku zarówno w trybie skryptu, jak i w spakowanym EXE (PyInstaller)."""
    if getattr(sys, "frozen", False):
        # katalog tymczasowy, do którego PyInstaller rozpakowuje zasoby przy --onefile
        base_path = sys._MEIPASS
    else:
        # podczas uruchamiania jako skrypt
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#PARAMETRY OKRESOWE STEROWANE Z KLAWIATURY
#1. Opisy parametrów (PL + EN)

desc_amp_A_pl = "Amplituda sezonowa alg. Wyższa = większe wahania."
desc_amp_A_en = "Seasonal amplitude of algae. Higher = stronger oscillations."

desc_amp_K_pl = "Amplituda sezonowa kryla. Wyższa = większe wahania."
desc_amp_K_en = "Seasonal amplitude of krill. Higher = stronger oscillations."

desc_amp_P_pl = "Amplituda sezonowa ryb (icefish). Wyższa = większe wahania."
desc_amp_P_en = "Seasonal amplitude of fish. Higher = stronger oscillations."

desc_habitat_K_pl = "Korekta siedliskowa kryla (100 = ogromne siedlisko)."
desc_habitat_K_en = "Krill habitat correction (100 = huge habitat)."

desc_habitat_P_pl = "Korekta siedliskowa icefish (1 = małe siedlisko)."
desc_habitat_P_en = "Icefish habitat correction (1 = small habitat)."

desc_damping_pl = "Siła tłumienia dynamicznego amplitudy (0–1)."
desc_damping_en = "Dynamic damping strength (0–1)."


#2. Pobieranie parametrów z klawiatury
print("\n=== Parametry modelu okresowego ===")

amp_A = ask_param("Amplituda alg", 0.20, desc_amp_A_pl, desc_amp_A_en)
amp_K = ask_param("Amplituda kryla", 0.15, desc_amp_K_pl, desc_amp_K_en)
amp_P = ask_param("Amplituda ryb", 0.12, desc_amp_P_pl, desc_amp_P_en)

habitat_kryl = ask_param("Siedlisko kryla (100)", 100.0, desc_habitat_K_pl, desc_habitat_K_en)
habitat_icefish = ask_param("Siedlisko icefish (1)", 1.0, desc_habitat_P_pl, desc_habitat_P_en)

damping_strength = ask_param("Tłumienie dynamiczne", 1.0, desc_damping_pl, desc_damping_en)



# ------------------------------
# ŚREDNIE CCAMLR (0–1)
# ------------------------------
K_mean_cc = 0.60
A_mean_cc = 0.80
B_mean_cc = 0.60
F_mean_cc = 0.50
P_mean_cc = 0.15

# MINIMA CCAMLR (0–1)
K_min_cc = 0.30
A_min_cc = 0.40
B_min_cc = 0.30
F_min_cc = 0.20
P_min_cc = 0.05

# ------------------------------
# PRZELICZENIE NA 0–1000
# ------------------------------
scale = 1000.0

K_mean_E = K_mean_cc * scale
A_mean_E = A_mean_cc * scale
B_mean_E = B_mean_cc * scale
F_mean_E = F_mean_cc * scale
P_mean_E = P_mean_cc * scale

K_min_E = K_min_cc * scale
A_min_E = A_min_cc * scale
B_min_E = B_min_cc * scale
F_min_E = F_min_cc * scale
P_min_E = P_min_cc * scale

# Europa
K_mean_M = 0.50 * scale
A_mean_M = 0.70 * scale
B_mean_M = 0.55 * scale
F_mean_M = 0.45 * scale
P_mean_M = 0.20 * scale

K_min_M = 0.25 * scale
A_min_M = 0.35 * scale
B_min_M = 0.30 * scale
F_min_M = 0.25 * scale
P_min_M = 0.08 * scale

# ------------------------------
# CZAS
# ------------------------------
t0, t_end = 0.0, 1500.0
dt = 1.0
N = int((t_end - t0) / dt) + 1
t = np.linspace(t0, t_end, N)

# ------------------------------
# SIEDLISKA (korekta amplitudy)
# ------------------------------
habitat_kryl = 100.0
habitat_algae = 100.0
habitat_bacteria = 100.0

habitat_icefish = 1.0
habitat_corals = 1.0

# ------------------------------
# FEEDBACK AMPLITUDE – ekologiczne + siedliskowe + dynamiczne
# ------------------------------
def dynamic_damping(X, target):
    """Amplituda maleje, gdy biomasa spada poniżej średniej."""
    ratio = X / target
    return np.clip(ratio, 0.0, 1.0)

def feedback_amplitude(X, X_min, X_max, habitat_factor, target):
    """
    1. ekologiczny dzwon (największa amplituda w środku zakresu)
    2. korekta siedliskowa (kryl 100× mniej wrażliwy)
    3. dynamiczne tłumienie amplitudy (gdy X << target)
    """
    # ekologiczny dzwon
    x = (X - X_min) / (X_max - X_min)
    x = np.clip(x, 0.0, 1.0)
    eco = 4.0 * x * (1.0 - x)

    # siedlisko
    habitat = 1.0 / habitat_factor


    # dynamiczne tłumienie
    #dyn = dynamic_damping(X, target)
    dyn = dynamic_damping(X, target) ** damping_strength

    return eco * habitat * dyn

# ------------------------------
# OKRESY I FAZY
# ------------------------------
T_year_E = 365.0
T_multi_E = 365.0 * 4.0

T_year_M = 500.0
T_multi_M = 500.0 * 4.0

phi_A_E = 0.0
phi_K_E = np.pi / 6.0
phi_P_E = np.pi / 3.0
phi_B_E = np.pi * 2.0 / 3.0
phi_F_E = np.pi / 2.0

phi_A_M = np.pi / 8.0
phi_K_M = np.pi / 4.0
phi_P_M = np.pi / 2.5
phi_B_M = np.pi * 3.0 / 4.0
phi_F_M = np.pi / 2.0

# ------------------------------
# FUNKCJE OKRESOWE – ZIEMIA (z feedbackiem)
# ------------------------------
def periodic_A_E(ti, A_target, A_current):
    season = np.sin(2*np.pi*ti/T_year_E + phi_A_E)
    multi  = np.sin(2*np.pi*ti/T_multi_E + phi_A_E/2.0)
    amp_fb = feedback_amplitude(A_current, A_min_E, scale, habitat_algae, A_target)
    return (amp_A*season + 0.10*multi) * A_target * amp_fb
    #return (0.20*season + 0.10*multi) * A_target * amp_fb

def periodic_K_E(ti, K_target, K_current):
    season = np.sin(2*np.pi*ti/T_year_E + phi_K_E)
    multi  = np.sin(2*np.pi*ti/T_multi_E + phi_K_E/2.0)
    amp_fb = feedback_amplitude(K_current, K_min_E, scale, habitat_kryl, K_target)
    return (amp_K*season + 0.08*multi) * K_target * amp_fb

def periodic_P_E(ti, P_target, P_current):
    season = np.sin(2*np.pi*ti/T_year_E + phi_P_E)
    multi  = np.sin(2*np.pi*ti/T_multi_E + phi_P_E/2.0)
    amp_fb = feedback_amplitude(P_current, P_min_E, scale, habitat_icefish, P_target)
    return (amp_P*season + 0.06*multi) * P_target * amp_fb

def periodic_B_E(ti, B_target, B_current):
    season = np.sin(2*np.pi*ti/T_year_E + phi_B_E)
    multi  = np.sin(2*np.pi*ti/(T_multi_E*1.5) + phi_B_E/2.0)
    amp_fb = feedback_amplitude(B_current, B_min_E, scale, habitat_bacteria, B_target)
    return (0.10*season + 0.05*multi) * B_target * amp_fb

def periodic_F_E(ti, F_target, F_current):
    multi = np.sin(2*np.pi*ti/(T_multi_E*2.0) + phi_F_E)
    amp_fb = feedback_amplitude(F_current, F_min_E, scale, habitat_corals, F_target)
    return 0.08 * multi * F_target * amp_fb

# ------------------------------
# FUNKCJE OKRESOWE – EUROPA (z feedbackiem)
# ------------------------------
def periodic_A_M(ti, A_target, A_current):
    season = np.sin(2*np.pi*ti/T_year_M + phi_A_M)
    multi  = np.sin(2*np.pi*ti/T_multi_M + phi_A_M/2.0)
    amp_fb = feedback_amplitude(A_current, A_min_M, scale, habitat_algae, A_target)
    return (0.22*season + 0.12*multi) * A_target * amp_fb

def periodic_K_M(ti, K_target, K_current):
    season = np.sin(2*np.pi*ti/T_year_M + phi_K_M)
    multi  = np.sin(2*np.pi*ti/T_multi_M + phi_K_M/2.0)
    amp_fb = feedback_amplitude(K_current, K_min_M, scale, habitat_kryl, K_target)
    return (0.16*season + 0.09*multi) * K_target * amp_fb

def periodic_P_M(ti, P_target, P_current):
    season = np.sin(2*np.pi*ti/T_year_M + phi_P_M)
    multi  = np.sin(2*np.pi*ti/T_multi_M + phi_P_M/2.0)
    amp_fb = feedback_amplitude(P_current, P_min_M, scale, habitat_icefish, P_target)
    return (0.13*season + 0.07*multi) * P_target * amp_fb

def periodic_B_M(ti, B_target, B_current):
    season = np.sin(2*np.pi*ti/T_year_M + phi_B_M)
    multi  = np.sin(2*np.pi*ti/(T_multi_M*1.5) + phi_B_M/2.0)
    amp_fb = feedback_amplitude(B_current, B_min_M, scale, habitat_bacteria, B_target)
    return (0.11*season + 0.06*multi) * B_target * amp_fb

def periodic_F_M(ti, F_target, F_current):
    multi = np.sin(2*np.pi*ti/(T_multi_M*2.0) + phi_F_M)
    amp_fb = feedback_amplitude(F_current, F_min_M, scale, habitat_corals, F_target)
    return 0.09 * multi * F_target * amp_fb

# ------------------------------
# PARAMETRY ŻEROWANIA
# ------------------------------
g_PK_E = 0.0003
g_KA_E = 0.0002
g_FB_E = 0.0002
g_PF_E = 0.0001

k_relax_K_E = 0.02
k_relax_A_E = 0.02
k_relax_B_E = 0.02
k_relax_F_E = 0.01
k_relax_P_E = 0.01

g_PK_M = 0.00025
g_KA_M = 0.00018
g_FB_M = 0.00022
g_PF_M = 0.00012

k_relax_K_M = 0.018
k_relax_A_M = 0.018
k_relax_B_M = 0.018
k_relax_F_M = 0.012
k_relax_P_M = 0.012

# ------------------------------
# RÓWNANIA – ZIEMIA
# ------------------------------
def step_biomass_E(ti, X):
    K, A, B, F, P = X

    fA = periodic_A_E(ti, A_mean_E, A)
    fK = periodic_K_E(ti, K_mean_E, K)
    fP = periodic_P_E(ti, P_mean_E, P)
    fB = periodic_B_E(ti, B_mean_E, B)
    fF = periodic_F_E(ti, F_mean_E, F)

    dK_relax = -k_relax_K_E * (K - K_mean_E)
    dA_relax = -k_relax_A_E * (A - A_mean_E)
    dB_relax = -k_relax_B_E * (B - B_mean_E)
    dF_relax = -k_relax_F_E * (F - F_mean_E)
    dP_relax = -k_relax_P_E * (P - P_mean_E)

    loss_K = g_PK_E * P * K
    loss_A = g_KA_E * K * A
    loss_B = g_FB_E * F * B
    loss_F = g_PF_E * P * F

    dK = dK_relax + fK - loss_K
    dA = dA_relax + fA - loss_A
    dB = dB_relax + fB - loss_B
    dF = dF_relax + fF - loss_F
    dP = dP_relax + fP

    return np.array([dK, dA, dB, dF, dP])

# ------------------------------
# RÓWNANIA – EUROPA
# ------------------------------
def step_biomass_M(ti, X):
    K, A, B, F, P = X

    fA = periodic_A_M(ti, A_mean_M, A)
    fK = periodic_K_M(ti, K_mean_M, K)
    fP = periodic_P_M(ti, P_mean_M, P)
    fB = periodic_B_M(ti, B_mean_M, B)
    fF = periodic_F_M(ti, F_mean_M, F)

    dK_relax = -k_relax_K_M * (K - K_mean_M)
    dA_relax = -k_relax_A_M * (A - A_mean_M)
    dB_relax = -k_relax_B_M * (B - B_mean_M)
    dF_relax = -k_relax_F_M * (F - F_mean_M)
    dP_relax = -k_relax_P_M * (P - P_mean_M)

    loss_K = g_PK_M * P * K
    loss_A = g_KA_M * K * A
    loss_B = g_FB_M * F * B
    loss_F = g_PF_M * P * F

    dK = dK_relax + fK - loss_K
    dA = dA_relax + fA - loss_A
    dB = dB_relax + fB - loss_B
    dF = dF_relax + fF - loss_F
    dP = dP_relax + fP

    return np.array([dK, dA, dB, dF, dP])

# ------------------------------
# INTEGRACJA – BEZ UCIĘĆ
# ------------------------------
def integrate_system(t, X0, step_func):
    X = np.zeros((len(t), 5))
    X[0] = X0
    for i in range(len(t)-1):
        dX = step_func(t[i], X[i])
        X[i+1] = X[i] + dX
        X[i+1] = np.maximum(X[i+1], 0)  # tylko zabezpieczenie przed wartościami ujemnymi
    return X

# ------------------------------
# START
# ------------------------------
X_E = integrate_system(t, np.array([K_mean_E, A_mean_E, B_mean_E, F_mean_E, P_mean_E]), step_biomass_E)
X_M = integrate_system(t, np.array([K_mean_M, A_mean_M, B_mean_M, F_mean_M, P_mean_M]), step_biomass_M)

K_E, A_E, B_E, F_E, P_E = X_E.T
K_M, A_M, B_M, F_M, P_M = X_M.T

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
ax1.set_xlabel("Time [⋅10² d]", loc='left')

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
        int(max(B_E.max(), F_E.max(), P_E.max()) * 1.2),
        6
    )
)
ax1_right.set_yticks(
    np.linspace(
        0,
        int(max(A_E.max()*3, K_E.max()*3) * 1.2),
        6
    )
)

ax1.set_ylabel(
    r"$Biomass_{\mathrm{normalized}}ᴮᵃᶜᵗᵉʳⁱᵉˢᴗᶜᵒˡᵈ ᶜᵒʳᵃˡˢᴗ³ᴵᶜᵉᶠⁱˢʰ$ "
    r"($B³ᴵᶜᵉᶠⁱˢʰₙₒᵣₘ[⋅2.45t⋅km⁻²] \mathrm{ } \approx  [⋅1934ind⋅km⁻²]$)",
    loc='top'
)

# --- Ikony Earth ---
ax1.add_artist(AnnotationBbox(OffsetImage(plt.imread(resource_path("p_georgianus.png")), zoom=0.25),
                              (0.90, 0.07), xycoords='axes fraction', frameon=False))
ax1.text(0.85, 0.06, "\n55 cm TL\n1795 g",
         ha='center', va='top', fontsize=8, transform=ax1.transAxes)
ax1.text(0.69, 0.03, "██████", color='black', fontsize=9, fontweight='bold', transform=ax1.transAxes)

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
        int(max(B_M.max(), F_M.max(), P_M.max()) * 1.2),
        6
    )
)
ax2_right.set_yticks(
    np.linspace(
        0,
        int(max(A_M.max()*3, K_M.max()*3) * 1.2),
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
fig.text(0.29, 0.03, "Bᴵᶜᵉᴬˡᵍᵃᵉₙₒᵣₘ▬▬▬▬▬[⋅37t⋅km⁻²]", color='green', fontsize=9, fontweight='bold')
fig.text(0.45, 0.03, "Bᴷʳⁱˡˡₙₒᵣₘ██████[⋅40t⋅km⁻²]", color='red', fontsize=9, fontweight='bold')
fig.text(0.59, 0.03, "Bᶜᵒˡᵈ ᶜᵒʳᵃˡˢₙₒᵣₘ██████[⋅0.16t⋅km⁻²]", color='lightskyblue', fontsize=9, fontweight='bold')
fig.text(0.77, 0.03, "B³ᴵᶜᵉᶠⁱˢʰₙₒᵣₘ██████[(0.45+0.5+1.5)t⋅km⁻²]", color='black', fontsize=9, fontweight='bold')

# ------------------------------
# ANIMACJA
# ------------------------------
def update(frame):
    ts = t[:frame]

    # Earth
    line_A_e.set_data(ts, A_E[:frame] * 5)     # algi ×3
    line_K_e.set_data(ts, K_E[:frame] * 6)     # kryl ×3
    line_P_e.set_data(ts, P_E[:frame] / 3)     # icefish ÷3
    line_B_e.set_data(ts, B_E[:frame] * 3)     # bakterie bez zmian
    line_F_e.set_data(ts, F_E[:frame] * 2)         # korale bez zmian
   
    # Europa
    line_B_m.set_data(ts, B_M[:frame])
    line_F_m.set_data(ts, F_M[:frame])
    line_P_m.set_data(ts, P_M[:frame] / 3)
    line_A_m.set_data(ts, A_M[:frame] * 3)
    line_K_m.set_data(ts, K_M[:frame] * 3)

    return (
        line_B_e, line_F_e, line_P_e, line_A_e, line_K_e,
        line_B_m, line_F_m, line_P_m, line_A_m, line_K_m
    )

anim = FuncAnimation(fig, update, frames=N, interval=20, blit=True)
plt.show()

print("\nAnimacja została zamknięta/Animation end.")
input("Naciśnij ENTER, aby przejść do opcji zapisu ENTER to saving option (GIF/MP4/XLSX/CSV)...")

# ============================
# ZAPIS ANIMACJI DO GIF
# ============================
save_gif = input("Zapisać animację do GIF? Save animation to GIF? (t/n): ").lower()

if save_gif == "t":
    import datetime
    import time
    import threading

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"animacja_biomasy_{timestamp}.gif"

    print(f"Zapisuję/Saving GIF jako/as: {filename}")
    print("Postęp zapisu/Saving... (gwiazdka/star = minęła 1 minuta/minute): ", end="")
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

    print("\nZapis zakończony/done.")


# ============================
# ZAPIS ANIMACJI DO MP4
# ============================
save_mp4 = input("Zapisać animację do MP4? Save animation in MP4? (t/n): ").lower()

if save_mp4 == "t":
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_mp4 = f"animacja_biomasy_{timestamp}.mp4"

    print(f"Zapisuję/Saving MP4 jako/as: {filename_mp4}")

    try:
        anim.save(filename_mp4, writer="ffmpeg", fps=20)
        print("Plik MP4 zapisany/done.")
    except Exception as e:
        print("Błąd podczas zapisu/error MP4:", e)


# ============================
# ZAPIS PARAMETRÓW DO TXT
# ============================
save_params = input("Zapisać parametry do pliku TXT? All data in TXT? (t/n): ").lower()

if save_params == "t":
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"parametry_{timestamp}.txt"
    
    with open(fname, "w", encoding="utf-8") as f:
    #with open(fname, "w") as f:
        f.write("=== Parametry okresowe ===\n")
        f.write(f"amp_A = {amp_A}\n")
        f.write(f"amp_K = {amp_K}\n")
        f.write(f"amp_P = {amp_P}\n")
        f.write(f"habitat_kryl = {habitat_kryl}\n")
        f.write(f"habitat_icefish = {habitat_icefish}\n")
        f.write(f"damping_strength = {damping_strength}\n")

        f.write("\n=== Parametry modelu Ziemi ===\n")
        f.write(f"K_mean_E = {K_mean_E}\n")
        f.write(f"A_mean_E = {A_mean_E}\n")
        f.write(f"B_mean_E = {B_mean_E}\n")
        f.write(f"F_mean_E = {F_mean_E}\n")
        f.write(f"P_mean_E = {P_mean_E}\n")

        f.write("\n=== Parametry modelu Europy ===\n")
        f.write(f"K_mean_M = {K_mean_M}\n")
        f.write(f"A_mean_M = {A_mean_M}\n")
        f.write(f"B_mean_M = {B_mean_M}\n")
        f.write(f"F_mean_M = {F_mean_M}\n")
        f.write(f"P_mean_M = {P_mean_M}\n")

    print(f"Parametry zapisane do pliku: {fname}")


# ============================
# ZAPIS PRZEBIEGÓW DO XLSX
# ============================
save_xlsx = input("Zapisać wszystkie przebiegi do jednego pliku XLSX? All data in xlsx? (t/n): ").lower()

if save_xlsx == "t":
    import datetime
    import pandas as pd

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    xlsx_name = f"wszystko_{timestamp}.xlsx"

    print(f"Zapisuję wszystkie przebiegi do pliku: {xlsx_name}")

    df = pd.DataFrame({
        "czas": t,
        "B_E": B_E,
        "F_E": F_E,
        "P_E": P_E,
        "A_E": A_E,
        "K_E": K_E,

        "B_M": B_M,
        "F_M": F_M,
        "P_M": P_M,
        "A_M": A_M,
        "K_M": K_M,

        "dB": B_M - B_E,
        "dF": F_M - F_E,
        "dP": P_M - P_E,
        "dA": A_M - A_E,
        "dK": K_M - K_E
    })

    df.to_excel(xlsx_name, index=False)
    print("Plik XLSX zapisany.")


# ============================
# ZAPIS PRZEBIEGÓW DO CSV
# ============================
save_csv_all = input("Zapisać wszystkie przebiegi do jednego pliku CSV? All data in CSV? (t/n): ").lower()

if save_csv_all == "t":
    import datetime, csv
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_name = f"wszystko_{timestamp}.csv"

    print(f"Zapisuję wszystkie przebiegi do pliku: {csv_name}")
    
    with open(csv_name, "w", newline="", encoding="utf-8") as csvfile:

    #with open(csv_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "czas",
            "B_E", "F_E", "P_E", "A_E", "K_E",
            "B_M", "F_M", "P_M", "A_M", "K_M",
            "dB", "dF", "dP", "dA", "dK"
        ])

        for i in range(len(t)):
            writer.writerow([
                t[i],
                B_E[i], F_E[i], P_E[i], A_E[i], K_E[i],
                B_M[i], F_M[i], P_M[i], A_M[i], K_M[i],
                B_M[i] - B_E[i],
                F_M[i] - F_E[i],
                P_M[i] - P_E[i],
                A_M[i] - A_E[i],
                K_M[i] - K_E[i]
            ])

    print("Plik CSV zapisany.")

print("Program zakończony / end.")
os._exit(0)

