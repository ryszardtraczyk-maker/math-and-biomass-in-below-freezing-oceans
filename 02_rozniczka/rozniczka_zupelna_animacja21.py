# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 21:26:42 2026

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import datetime
import os
import matplotlib
matplotlib.use("Qt5Agg")

# ==========================================
# 1. PRZYGOTOWANIE DANYCH
# ==========================================
x = np.linspace(-1.5, 1.5, 120)
y = np.linspace(-1.5, 1.5, 120)
X, Y = np.meshgrid(x, y)

Z_licznik = X * Y
Z_mianownik = X**2 + Y**2
Z_wynik = np.zeros_like(X)
maska = (X**2 + Y**2) > 0
Z_wynik[maska] = Z_licznik[maska] / Z_mianownik[maska]

x_linia = np.linspace(-1.5, 1.5, 100)
z_linia_licznik = x_linia * 1.5
z_linia_mianownik_baza = 1 * x_linia**2 + 2.25  
z_linia_wynik = z_linia_licznik / z_linia_mianownik_baza
y_sciana = np.ones_like(x_linia) * 1.5

ELEV_START = 5
ELEV_FINAL = 25
AZIM_STAŁY = 15

# Przebudowany tekst naukowy (szersze linie, krótsza wysokość bloku)
pelny_wywod_matematyczny = (
    r"$\bf{KONTRPRZYKŁAD\ MATEMATYCZNY:}$" + "\n"
    "Jeśli funkcja jest zbudowana z podstawowych funkcji ciągłych\n"
    "(wielomiany, trygonometria) za pomocą dodawania, mnożenia czy składania,\n"
    "to z automatu jest ciągła w całej swojej dziedzinie, po całej powierzchni)!\n\n"
    r"Powierzchnia: $Z₁ = X \cdot Y$ i profil: $y₁=1.5$, $z₁ = x \cdot 1.5$" + "\n"
    r"Powierzchnia: $Z₂ = X^2 + Y^2$ i profil: $y₂=1.5$, $z₂ = x^2 + 2.25$" + "\n"
    r"Złożenie powierzchni: $Z₃ = \frac{X \cdot Y}{X^2 + Y^2}$ i profili: $y₃=1.5$, $z₃ = \frac{x \cdot 1.5}{x^2 + 2.25}$" + "\n\n"
    "Iloraz dwóch płaszczyzn (ciągłych i różniczkowalnych) tworzy płaszczyznę,\n"
    "która posiada pochodne cząstkowe w punkcie (0,0) równe 0. Funkcja jest\n"
    "więc ciągła wzdłuż osi X oraz Y. Ale na skosie w tym punkcie ma granicę\n"
    r"$\frac{1}{2}$ $\neq$ 0. Nie jest więc ciągła w punkcie (0,0), czyli posiada tam nieciągłość" + "\n\n"
    "Przenikanie geometryczne (rogi płaszczyzn składowych ciągnące\n"
    "w przeciwne strony) obrazuje przyczynę i mechanizm rozdarcia.\n\n"
    "Kliknij po więcej..."
)

start_clicked = False  
offset_licznik_start = 11.25
offset_mianownik_start = 3.5
offset_stop_fuzji = offset_mianownik_start + 2.50 

# Tworzenie okna
fig = plt.figure(figsize=(16, 9))

# ZMIANA 1: Maksymalne rozciągnięcie wykresu w lewo i w pionie (szerokość z 0.75 na 0.82, wysokość z 0.90 na 0.96)
# Przesunęliśmy wykres na przeciwną stronę (X z 0.05 na -0.05), dając gigantyczną przestrzeń na bryły
ax = fig.add_axes([-0.05, 0.02, 0.82, 0.96], projection='3d')

ax.xaxis.set_pane_color((1,1,1,0))
ax.yaxis.set_pane_color((1,1,1,0))
ax.zaxis.set_pane_color((1,1,1,0))
ax.set_zlim(-1.0, 13.5)

# Renderowanie makiety początkowej
surf1 = ax.plot_surface(X, Y, Z_licznik + offset_licznik_start, cmap='coolwarm', edgecolor='none', alpha=0.5)
line1, = ax.plot(x_linia, y_sciana, z_linia_licznik + offset_licznik_start, color='red', linewidth=3)
surf2 = ax.plot_surface(X, Y, Z_mianownik + offset_mianownik_start, cmap='viridis', edgecolor='none', alpha=0.4)
line2, = ax.plot(x_linia, y_sciana, z_linia_mianownik_baza + offset_mianownik_start, color='green', linewidth=3)
surf3 = ax.plot_surface(X, Y, Z_wynik, cmap='coolwarm', edgecolor='none', alpha=0.8)
line3, = ax.plot(x_linia, y_sciana, z_linia_wynik, color='darkblue', linewidth=3)
surf4 = ax.plot_surface(X, Y, Z_wynik, cmap='coolwarm', edgecolor='none', alpha=0.0)

ax.set_xlabel('Oś X', labelpad=-5, fontsize=10)
ax.set_ylabel('Oś Y', labelpad=-5, fontsize=10)
ax.set_zlabel('Oś Z', labelpad=-5, fontsize=10)
ax.tick_params(axis='both', which='major', labelsize=8, pad=-2)
ax.view_init(elev=ELEV_START, azim=AZIM_STAŁY)

# ZMIANA 2: Umieszczenie wydłużonego, niskiego bloku tekstowego tuż obok grafiki za pomocą fig.text
# Pozycja X=0.62 (dosunięty do grafiki), Y=0.22 (wyśrodkowany pionowo), ma mniejszą wysokość struktury
tekst_naukowy = fig.text(0.60, 0.50, pelny_wywod_matematyczny, fontsize=10, va='center', ha='left',
                         linespacing=1.3, bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray', boxstyle='round,pad=0.5'))

# ==========================================
# 2. SEKWENCYJNA ARCHITEKTURA KLATEK
# ==========================================
def dynamic_render(ruch_frame):
    global surf1, surf2, surf3, surf4, line1, line2, line3

    if ruch_frame <= 40:
        t_fuzja = (1 - np.cos(ruch_frame / 40 * np.pi)) / 2
        t_zaginanie = 0.0
        t_transmutacja = 0.0
        t_freeze = 0.0
    elif 40 < ruch_frame <= 70:
        t_fuzja = 1.0
        t_zaginanie = (1 - np.cos((ruch_frame - 40) / 30 * np.pi)) / 2
        t_transmutacja = 0.0
        t_freeze = 0.0
    elif 70 < ruch_frame <= 85:
        t_fuzja = 1.0
        t_zaginanie = 1.0
        t_transmutacja = (ruch_frame - 70) / 15  
        t_freeze = 0.0
    elif 85 < ruch_frame <= 125:
        t_fuzja = 1.0
        t_zaginanie = 1.0
        t_transmutacja = 1.0
        t_freeze = 1.0
    else:
        t_fuzja = 1.0 - (ruch_frame - 125) / 10
        t_zaginanie = 1.0 - (ruch_frame - 125) / 10
        t_transmutacja = 1.0 - (ruch_frame - 125) / 10
        t_freeze = 0.0

    current_offset_licznik = offset_licznik_start - (offset_licznik_start - offset_stop_fuzji) * t_fuzja
    current_offset_mianownik = offset_mianownik_start

    surf1.remove()
    surf1 = ax.plot_surface(X, Y, Z_licznik + current_offset_licznik, cmap='coolwarm', edgecolor='none', alpha=0.5 * (1 - t_transmutacja))
    if t_transmutacja > 0.0:
        line1.set_data_3d([], [], [])
    else:
        line1.set_data_3d(x_linia, y_sciana, z_linia_licznik + current_offset_licznik)
    
    surf2.remove()
    Z_mianownik_dynamiczny = Z_mianownik.copy()
    maska_zaginania = (X * Y < 0)
    Z_mianownik_dynamiczny[maska_zaginania] = Z_mianownik[maska_zaginania] * (1 - 0.9 * t_zaginanie)
    surf2 = ax.plot_surface(X, Y, Z_mianownik_dynamiczny + current_offset_mianownik, cmap='viridis', edgecolor='none', alpha=0.4 * (1 - t_transmutacja))
    
    if t_zaginanie > 0.0:
        line2.set_data_3d([], [], [])
    else:
        line2.set_data_3d(x_linia, y_sciana, z_linia_mianownik_baza + current_offset_mianownik)

    if t_transmutacja > 0.0:
        line3.set_data_3d([], [], [])
    else:
        line3.set_data_3d(x_linia, y_sciana, z_linia_wynik)
    surf3.set_alpha(max(0, 0.8 * (1 - t_transmutacja)))

    surf4.remove()
    if t_freeze > 0.0:
        ax.set_zlim(-0.6, 0.6)
        ax.view_init(elev=ELEV_FINAL, azim=AZIM_STAŁY)
        surf4 = ax.plot_surface(X, Y, Z_wynik, cmap='coolwarm', edgecolor='none', alpha=0.8)
    else:
        ax.set_zlim(-1.0, 13.5)
        ax.view_init(elev=ELEV_START, azim=AZIM_STAŁY)
        surf4 = ax.plot_surface(X, Y, Z_wynik + current_offset_mianownik, cmap='coolwarm', edgecolor='none', alpha=0.8 * t_transmutacja)

def update_screen(frame):
    dynamic_render(frame)
    return surf1, surf2, surf3, surf4

# ==========================================
# 3. INTERAKCJA EKRANOWA
# ==========================================
def templates_start(event):
    global start_clicked, ani
    if not start_clicked:
        start_clicked = True
        fig.canvas.mpl_disconnect(cid_key)
        fig.canvas.mpl_disconnect(cid_mouse)
        
        # Zmiana tekstu w boksie po kliknięciu (usuwamy instrukcję "Kliknij po więcej")
        tekst_w_ruchu = pelny_wywod_matematyczny.replace("Kliknij po więcej...", "Trwa fuzja geometrii...")
        tekst_naukowy.set_text(tekst_w_ruchu)
        
        ani = FuncAnimation(fig, update_screen, frames=135, interval=35, blit=False, repeat=True)
        fig.canvas.draw()

cid_key = fig.canvas.mpl_connect('key_press_event', templates_start)
cid_mouse = fig.canvas.mpl_connect('button_press_event', templates_start)

print("[INFO] Program gotowy. Kliknij okno wykresu, aby uruchomić fuzję.")
plt.show()

# ==========================================
# 4. EXPORT DO PLIKÓW
# ==========================================
save_choice = input("Czy zapisać animację do pliku? (t/n): ").strip().lower()
if save_choice != "t":
    print("Pomijam zapis pliku.")
    os._exit(0)

print("[INFO] Przygotowuję klatki i tekst do zapisu...")
surf1.remove(); surf2.remove(); surf4.remove()
surf1 = ax.plot_surface(X, Y, Z_licznik + offset_licznik_start, cmap='coolwarm', edgecolor='none', alpha=0.5)
surf2 = ax.plot_surface(X, Y, Z_mianownik + offset_mianownik_start, cmap='viridis', edgecolor='none', alpha=0.4)
line1.set_data_3d(x_linia, y_sciana, z_linia_licznik + offset_licznik_start)
line2.set_data_3d(x_linia, y_sciana, z_linia_mianownik_baza + offset_mianownik_start)
line3.set_data_3d(x_linia, y_sciana, z_linia_wynik)
surf3.set_alpha(0.8)
surf4 = ax.plot_surface(X, Y, Z_wynik, cmap='coolwarm', edgecolor='none', alpha=0.0)
ax.set_zlim(-1.0, 13.5)
ax.view_init(elev=ELEV_START, azim=AZIM_STAŁY)

file_ani = FuncAnimation(fig, update_screen, frames=135, interval=100, blit=False, repeat=False)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
mp4_name = f"kontrprzyklad_ciaglosc_{timestamp}.mp4"
gif_name = f"kontrprzyklad_ciaglosc_{timestamp}.gif"

print(f"Zapisuję prezentację do MP4 ({mp4_name}) i GIF ({gif_name})...")

try:
    file_ani.save(mp4_name, writer="ffmpeg", fps=10)
    print("Zapisano MP4 pomyślnie.")
except Exception as e:
    print("Błąd MP4:", e)

try:
    writer = PillowWriter(fps=10)
    file_ani.save(gif_name, writer=writer)
    print("Zapisano GIF pomyślnie.")
except Exception as e:
    print("Błąd GIF:", e)

print("Program zakończony / end.")
os._exit(0)