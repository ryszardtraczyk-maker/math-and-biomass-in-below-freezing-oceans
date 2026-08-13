# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 20:18:42 2026

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
matplotlib.use("Qt5Agg")
import sys
import os

# --- 1. INTERAKCJA PRZED URUCHOMIENIEM WYKRESU ---
print("="*60)
print(" DYNAMICZNA WIZUALIZACJA 3D: DEFINICJA CAUCHY'EGO")
print("="*60)
print("Sugerowane ustawienie widoku: Podniesienie (elev)=5, Azymut (azim)=12")
print("-"*60)

user_input = input("Wciśnij ENTER aby zaakceptować to ustawienie\nlub wpisz własne jako 'podniesienie, azymut': ").strip()

if user_input == "":
    aktualny_elev = 5
    aktualny_azim = 12
else:
    try:
        e, a = map(float, user_input.split(','))
        aktualny_elev = e
        aktualny_azim = a
    except ValueError:
        print("Błędny format. Zastosowano domyślne kąty: 5, 12")
        aktualny_elev = 5
        aktualny_azim = 12

# --- 2. MAKSYMALIZACJA ROZMIARU RYSUNKU ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_axes([0.00, 0.10, 1.00, 0.90], projection='3d')
# Zmień dotychczasowe plt.subplots na wersję z określeniem wymiarów (szerokość, wysokość w calach)
#fig, ax = plt.subplots(figsize=(8, 7), subplot_kw={'projection': '3d'})

# Zmniejsza białe marginesy z każdej strony (wartości od 0 do 1)
#fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
#fig.tight_layout()
# --- 3. PARAMETRY GEOMETRYCZNE ORAZ SFERA ---
R = 0.5  # delta = 0.5
n = np.arange(1, 120)

# Uwyraźniona 1/8 sfery
u = np.linspace(0, np.pi / 2, 60)
v = np.linspace(0, np.pi / 2, 60)
x_sphere = R * np.outer(np.cos(u), np.sin(v))
y_sphere = R * np.outer(np.sin(u), np.sin(v))
z_sphere = R * np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x_sphere, y_sphere, z_sphere, color='royalblue', alpha=0.07, edgecolor='mediumblue', linewidth=0.25)

# Oznaczenie tekstowe promienia delta w przestrzeni blisko krawędzi sfery
ax.text(0.18, 0.32, 0.25, r'$\delta = 0.5$', color='mediumblue', fontsize=11, fontweight='bold')

# Wektory kierunkowe
vx, vy, vz = 1/np.sqrt(3), 1/np.sqrt(3), 1/np.sqrt(3)

# --- 4. ANALITYCZNE OBLICZENIA PUNKTÓW PRZECIĘCIA SFERY ---
tc = 0.5
sc_x, sc_y, sc_z = tc*vx, tc*vy, tc*vz

a_q = 1.0
b_q = 0.4 / np.sqrt(3)
c_q = 0.04 - 0.25
tp = (-b_q + np.sqrt(b_q**2 - 4*a_q*c_q)) / (2*a_q)
sp_x, sp_y, sp_z = tp*vx, tp*vy, tp*vz + 0.2

b_q_m = -0.4 / np.sqrt(3)
tm = (-b_q_m + np.sqrt(b_q_m**2 - 4*a_q*c_q)) / (2*a_q)
sm_x, sm_y, sm_z = tm*vx, tm*vy, tm*vz - 0.2

sf_x, sf_y, sf_z = 0.5/np.sqrt(2), 0.5/np.sqrt(2), 0.0

# --- 5. RYSOWANIE STATYCZNYCH ELEMENTÓW CIĄGÓW ---

# A) Główny
x_c = (1 / n) * vx; y_c = (1 / n) * vy; z_c = (1 / n) * vz
mask_c = (x_c <= 0.6) & (y_c <= 0.6) & (z_c <= 0.6)
ax.plot(np.insert(x_c[mask_c], 0, 0.6), np.insert(y_c[mask_c], 0, 0.6), np.insert(z_c[mask_c], 0, 0.6), color='red', linestyle=':', linewidth=1.5)
ax.plot(x_c[mask_c], y_c[mask_c], z_c[mask_c], color='red', linestyle='-', alpha=0.2)
ax.scatter(x_c[mask_c], y_c[mask_c], z_c[mask_c], color='red', marker='.', s=10, alpha=0.5)
ax.scatter(0.6, 0.6, 0.6, facecolors='none', edgecolors='red', marker='*', s=120, linewidths=1.2, zorder=5)
ax.scatter(sc_x, sc_y, sc_z, facecolors='none', edgecolors='red', marker='o', s=50, linewidths=1.5, zorder=6)
ax.text(0.57, 0.57, 0.62, r'$x_n = ⅟ₙ$', color='red', fontsize=10)

# B) Podniesiony
x_p = (1 / n) * vx; y_p = (1 / n) * vy; z_p = (1 / n) * vz + 0.2
mask_p = (x_p <= 0.6) & (y_p <= 0.6) & (z_p <= 0.6)
ax.plot(np.insert(x_p[mask_p], 0, 0.4), np.insert(y_p[mask_p], 0, 0.4), np.insert(z_p[mask_p], 0, 0.6), color='darkorange', linestyle=':', linewidth=1.5)
ax.plot(x_p[mask_p], y_p[mask_p], z_p[mask_p], color='darkorange', linestyle='-', alpha=0.2)
ax.scatter(x_p[mask_p], y_p[mask_p], z_p[mask_p], color='darkorange', marker='.', s=10, alpha=0.5)
ax.scatter(0.4, 0.4, 0.6, facecolors='none', edgecolors='darkorange', marker='*', s=120, linewidths=1.2, zorder=5)
ax.scatter(sp_x, sp_y, sp_z, facecolors='none', edgecolors='darkorange', marker='o', s=50, linewidths=1.5, zorder=6)
ax.text(0.35, 0.35, 0.63, r'$x_n = ⅟ₙ + 0.2$', color='darkorange', fontsize=10)

# C) Podłogowy (Płaski)
x_f = (1 / n) * (1/np.sqrt(2)); y_f = (1 / n) * (1/np.sqrt(2)); z_f = np.zeros_like(x_f)
mask_f = (x_f <= 0.6) & (y_f <= 0.6)
ax.plot(np.insert(x_f[mask_f], 0, 0.6), np.insert(y_f[mask_f], 0, 0.6), np.insert(z_f[mask_f], 0, 0.0), color='green', linestyle=':', linewidth=1.5)
ax.plot(x_f[mask_f], y_f[mask_f], z_f[mask_f], color='green', linestyle='-', alpha=0.2)
ax.scatter(x_f[mask_f], y_f[mask_f], z_f[mask_f], color='green', marker='.', s=10, alpha=0.5)
ax.scatter(0.6, 0.6, 0.0, facecolors='none', edgecolors='green', marker='*', s=120, linewidths=1.2, zorder=5)
ax.scatter(sf_x, sf_y, sf_z, facecolors='none', edgecolors='green', marker='o', s=50, linewidths=1.5, zorder=6)
ax.text(0.57, 0.47, 0.02, r'$x_n = ⅟ₙ \ (z=0)$', color='green', fontsize=10)

# D) Obniżony
x_m = (1 / n) * vx; y_m = (1 / n) * vy; z_m = (1 / n) * vz - 0.2
xp_podloga, yp_podloga, zp_podloga = 0.2, 0.2, 0.0
mask_m_nad = (x_m <= 0.6) & (y_m <= 0.6) & (z_m <= 0.6) & (z_m >= 0)
mask_m_pod = (z_m < 0)

ax.plot(np.insert(x_m[mask_m_nad], 0, 0.6), np.insert(y_m[mask_m_nad], 0, 0.6), np.insert(z_m[mask_m_nad], 0, 0.4), color='purple', linestyle=':', linewidth=1.5)
ax.plot(np.append(x_m[mask_m_nad], xp_podloga), np.append(y_m[mask_m_nad], yp_podloga), np.append(z_m[mask_m_nad], zp_podloga), color='purple', linestyle='-', alpha=0.2)
ax.scatter(x_m[mask_m_nad], y_m[mask_m_nad], z_m[mask_m_nad], color='purple', marker='.', s=10, alpha=0.5)
ax.scatter(0.6, 0.6, 0.4, facecolors='none', edgecolors='purple', marker='*', s=120, linewidths=1.2, zorder=5)
ax.scatter(sm_x, sm_y, sm_z, facecolors='none', edgecolors='purple', marker='o', s=50, linewidths=1.5, zorder=6)
ax.text(0.57, 0.57, 0.43, r'$x_n = ⅟ₙ - 0.2$', color='purple', fontsize=10)

# Część podziemna zasnuta
ax.plot(np.insert(x_m[mask_m_pod], 0, xp_podloga), np.insert(y_m[mask_m_pod], 0, yp_podloga), np.insert(z_m[mask_m_pod], 0, zp_podloga), color='purple', linestyle='--', alpha=0.12)
ax.scatter(x_m[mask_m_pod], y_m[mask_m_pod], z_m[mask_m_pod], color='purple', marker='.', s=10, alpha=0.15)

# --- 6. ELEMENTY OBJAŚNIAJĄCE DEFINICJĘ CAUCHY'EGO ---
xa_x, xa_y, xa_z = sc_x, sc_y, sc_z
xb_x, xb_y, xb_z = (1/4)*vx, (1/4)*vy, (1/4)*vz

# Rysowanie grubej linii odległości d(x_a, x_b)
ax.plot([xa_x, xb_x], [xa_y, xb_y], [xa_z, xb_z], color='black', linewidth=3.0, zorder=8)

# 1. Poprawione pozycje napisów w przestrzeni 3D
ax.text(xa_x + 0.05, xa_y, xa_z - 0.025, r'$x_a$', color='black', fontsize=11, fontweight='bold', zorder=9)
ax.text(xb_x + 0.05, xb_y, xb_z - 0.03, r'$x_b$', color='black', fontsize=11, fontweight='bold', zorder=9)

# Obniżone jeszcze bardziej (poprzednio było +0.01, teraz zmiana poszła dwa razy mocniej w dół)
ax.text((xa_x+xb_x)/2 + 0.04, (xa_y+xb_y)/2, (xa_z+xb_z)/2 - 0.04, r'$d(x_a, x_b) < \delta$', color='black', fontsize=10)


# Strzałka pionowa (j) wskazująca na punkt x_a na sferze
ax.quiver(xa_x, xa_y, xa_z + 0.09, 0, 0, -0.07, color='black', linewidth=1.0, arrow_length_ratio=0.3, zorder=9)
ax.text(xa_x, xa_y, xa_z + 0.10, r'$j$', color='black', fontsize=16, fontweight='bold', ha='center')

# --- 7. ZNAKI GRANIC I TEKST DEFINICJI NA ŚCIANIE ---
ax.scatter(0, 0, 0, color='black', marker='X', s=25, zorder=10)        
ax.scatter(0, 0, 0.2, color='black', marker='X', s=25, zorder=10) 
ax.scatter(0, 0, -0.2, color='black', marker='X', s=25, alpha=0.2, zorder=2) 

# Dodaj ten kod raz, poza funkcją animującą (będzie widoczny przez całą animację)
fig.text(0.5, 0.88, 'Kolejne wyrazy ciągu Cauchy’ego', transform=fig.transFigure, fontsize=12, fontweight='light', ha='center')

# Wklejenie tekstu definicji jako opis wewnętrzny na bocznej ścianie układu
definicja_txt = r"$\forall \delta>0 \ \exists j \in \mathbb{N} \ \forall a,b \geq j \Rightarrow d(x_a, x_b) < \delta$"
ax.text(0.02, 0.05, 0.52, definicja_txt, fontsize=12, color='black', bbox=dict(facecolor='none', alpha=0.7, edgecolor='none'))

# --- 8. USTAWIENIA TEKSTURY ŚCIAN I OSI ---
ax.xaxis.set_pane_color((0.94, 0.94, 0.94, 1.0))
ax.yaxis.set_pane_color((0.94, 0.94, 0.94, 1.0))
ax.zaxis.set_pane_color((0.89, 0.89, 0.89, 1.0))
ax.grid(True, linestyle='--', alpha=0.5, color='gray')

ax.set_xlim3d(0, 0.6)
ax.set_ylim3d(0, 0.6)
ax.set_zlim3d(0, 0.6)

ax.set_xlabel('Oś X')
ax.set_ylabel('Oś Y')
ax.set_zlabel('Oś Z')

ax.set_box_aspect((1, 1, 1))
ax.view_init(elev=aktualny_elev, azim=aktualny_azim)

# Zamiast r'$\star$' używamy u"\u2606" (gwiazdka bez wypełnienia)
fig.text(0.27, 0.143, u"\u2606", transform=fig.transFigure, fontsize=15, color='black', ha='center', va='center')
fig.text(0.33, 0.14, 'zasięg XYZ: 0.6', transform=fig.transFigure, fontsize=10, color='black', ha='center')
fig.text(0.44, 0.14, r'  ○   xₙ = δ = 0.5', transform=fig.transFigure, fontsize=10, color='blue', ha='center')
fig.text(0.54, 0.14, r'  ●   xₙ < δ', transform=fig.transFigure, fontsize=10, color='gray', ha='center')
fig.text(0.61, 0.14, r'  $\mathbf{}$×  $\lim x_n$', transform=fig.transFigure, fontsize=10, color='black', ha='center')

# --- 9. MODUŁ ANIMACJI ---
kroki_t = np.geomspace(1.0, 45.0, 60)

ani_c = ax.scatter([], [], [], facecolors='none', edgecolors='red', marker='o', s=120, linewidths=1.8, zorder=12)
ani_p = ax.scatter([], [], [], facecolors='none', edgecolors='darkorange', marker='o', s=120, linewidths=1.8, zorder=12)
ani_f = ax.scatter([], [], [], facecolors='none', edgecolors='green', marker='o', s=120, linewidths=1.8, zorder=12)
ani_m = ax.scatter([], [], [], facecolors='none', edgecolors='purple', marker='o', s=120, linewidths=1.8, zorder=12)

def update(frame):
    t = kroki_t[frame]
    
    # Główny
    cx, cy, cz = (1/t)*vx, (1/t)*vy, (1/t)*vz
    if cx > 0.6: cx, cy, cz = 0.6, 0.6, 0.6
    ani_c._offsets3d = ([cx], [cy], [cz])
    
    # Podniesiony
    px, py, pz = (1/t)*vx, (1/t)*vy, (1/t)*vz + 0.2
    if px > 0.4: px, py, pz = 0.4, 0.4, 0.6
    ani_p._offsets3d = ([px], [py], [pz])
    
    # Płaski
    fx, fy, fz = (1/t)*(1/np.sqrt(2)), (1/t)*(1/np.sqrt(2)), 0.0
    if fx > 0.6: fx, fy, fz = 0.6, 0.6, 0.0
    ani_f._offsets3d = ([fx], [fy], [fz])
    
    # Obniżony
    mx, my, mz = (1/t)*vx, (1/t)*vy, (1/t)*vz - 0.2
    if mx > 0.6: mx, my, mz = 0.6, 0.6, 0.4
    ani_m._offsets3d = ([mx], [my], [mz])
    
    return ani_c, ani_p, ani_f, ani_m

# Zapisanie obiektu animacji do zmiennej "anim"
anim = FuncAnimation(fig, update, frames=len(kroki_t), interval=60, blit=False, repeat=True)

print("\nUruchomiono animację przestrzennej zbieżności Cauchy'ego...")
plt.show()

# =============================================================================
# --- ZINTEGROWANY BLOK ZAPISU PLIKÓW (ZAMKNIĘCIE I EKSPORT) ---
# =============================================================================
import sys

print("\nAnimacja została zamknięta/Animation end.")
input("Naciśnij ENTER, aby przejść do opcji zapisu; ENTER to saving option (GIF/MP4)...")

# ============================
# ZAPIS ANIMACJI DO GIF
# ============================
save_gif = input("Zapisać animację do GIF? Save animation to GIF? (t/n): ").lower()

if save_gif == "t":
    import datetime
    import time
    import threading

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"animacja_cauchy_{timestamp}.gif"

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
        # Zapis za pomocą domyślnego kodu pillow (wbudowany w Matplotlib)
        anim.save(filename, writer="pillow", fps=20)
        print("\nZapis GIF zakończony/done.")
    except Exception as e:
        print("\nBłąd podczas zapisu GIF:", e)

    running = False
    star_thread_obj.join()


# ============================
# ZAPIS ANIMACJI DO MP4
# ============================
save_mp4 = input("Zapisać animację do MP4? Save animation in MP4? (t/n): ").lower()

if save_mp4 == "t":
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_mp4 = f"animacja_cauchy_{timestamp}.mp4"

    print(f"Zapisuję/Saving MP4 jako/as: {filename_mp4}")

    try:
        # Wymaga zainstalowanego pakietu ffmpeg w systemie
        anim.save(filename_mp4, writer="ffmpeg", fps=20)
        print("Plik MP4 zapisany/done.")
    except Exception as e:
        print("Błąd podczas zapisu/error MP4:", e)
        
    print("Program zakończony / end.")
os._exit(0)