# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 09:22:34 2026

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import datetime
import matplotlib
matplotlib.use("Qt5Agg")

# Funkcja pomocnicza do pobierania danych z klawiatury z domyślnym Enterem
def pobierz_parametr(komunikat, domyslny):
    wybor = input(f"{komunikat} [{domyslny}]: ").strip()
    return domyslny if wybor == "" else wybor

print("=== INTERAKTYWNY ANALIZATOR FUNKCJI ===")

# 1. WYBÓR FUNKCJI
print("\nWybierz funkcję do analizy:")
print("1: f(x) = x³ - x")
print("2: f(x) = x⁴ - 2x²")
print("3: f(x) = eˣ * (x - 1)")
print("4: f(x) = x⁵")
print("5: f(x) = x⁷ - 7x⁵")
print("6: f(x) = |x|³")
print("7: f(x) = sin(x)")
print("8: f(x) = cos(x)")
print("9: Własna funkcja (wpisywana wzorem Pythona)")

wybor_f = pobierz_parametr("Twój wybór (1-9)", "1")

if wybor_f == "1":
    f_mat = lambda x: x**3 - x
    fp_mat = lambda x: 3*x**2 - 1
    wzor_tekst = "f(x) = x³ - x"
elif wybor_f == "2":
    f_mat = lambda x: x**4 - 2*x**2
    fp_mat = lambda x: 4*x**3 - 4*x
    wzor_tekst = "f(x) = x⁴ - 2x²"
elif wybor_f == "3":
    f_mat = lambda x: np.exp(x) * (x - 1)
    fp_mat = lambda x: x * np.exp(x)
    wzor_tekst = "f(x) = eˣ * (x - 1)"
elif wybor_f == "4":
    f_mat = lambda x: x**5
    fp_mat = lambda x: 5*x**4
    wzor_tekst = "f(x) = x⁵"
elif wybor_f == "5":
    f_mat = lambda x: x**7 - 7*x**5
    fp_mat = lambda x: 7*x**6 - 35*x**4
    wzor_tekst = "f(x) = x⁷ - 7x⁵"
elif wybor_f == "6":
    f_mat = lambda x: np.abs(x)**3
    fp_mat = lambda x: 3 * x * np.abs(x)
    wzor_tekst = "f(x) = |x|³"
elif wybor_f == "7":
    f_mat = lambda x: np.sin(x)
    fp_mat = lambda x: np.cos(x)
    wzor_tekst = "f(x) = sin(x)"
elif wybor_f == "8":
    f_mat = lambda x: np.cos(x)
    fp_mat = lambda x: -np.sin(x)
    wzor_tekst = "f(x) = cos(x)"
else:
    print("\nWpisz wzór (np. x**2 - 4*x): ")
    wlasny_wzor = input("Wzór: ").strip()
    f_mat = lambda x: eval(wlasny_wzor)
    fp_mat = lambda x: (f_mat(x + 1e-5) - f_mat(x - 1e-5)) / 2e-5
    wzor_tekst = f"f(x) = {wlasny_wzor}"

# 2. PERSONALIZACJA WYGLĄDU ORAZ DECYZJA O EKSPORCIE (Z GÓRY)
print("\n--- Konfiguracja wyglądu wykresu ---")
kolor_wykresu = pobierz_parametr("Kolor wykresu głównego (np. blue, red, black)", "blue")
styl_stycznej = pobierz_parametr("Styl linii stycznej (-- przerywana, - ciągła)", "--")
kolor_stycznej = pobierz_parametr("Kolor linii stycznej (np. red, orange)", "red")
tytul_wykresu = pobierz_parametr("Tytuł wykresu", f"Dynamiczna analiza dla {wzor_tekst}")

print("\n--- Decyzja o zapisie wideo ---")
decyzja_gif = pobierz_parametr("Czy po zamknięciu wykresu wyeksportować automatycznie plik GIF? (t/n)", "n").lower()
decyzja_mp4 = pobierz_parametr("Czy po zamknięciu wykresu wyeksportować automatycznie plik MP4? (t/n)", "n").lower()

# 3. PRZYGOTOWANIE STRUKTURY OKNA INTERAKTYWNEGO (NA ŻYWO)
x_wielkie = np.linspace(-2.5, 2.5, 400)
y_wielkie = f_mat(x_wielkie)

plt.ion() # Włączenie trybu interaktywnego

fig, (ax, ax_info) = plt.subplots(2, 1, figsize=(9, 8), gridspec_kw={'height_ratios': [3, 1]})
fig.subplots_adjust(hspace=0.3)

ax.plot(x_wielkie, y_wielkie, color=kolor_wykresu, linewidth=2.5, label=wzor_tekst)
punkt, = ax.plot([], [], 'ro', markersize=8, label="Bieżący punkt (x₀, f(x₀))")
styczna_linia, = ax.plot([], [], color=kolor_stycznej, linestyle=styl_stycznej, linewidth=1.5, label="Styczna w x₀")

ax.axhline(0, color='black', linewidth=0.8, linestyle=':')
ax.axvline(0, color='black', linewidth=0.8, linestyle=':')
ax.grid(True, linestyle=':', alpha=0.5)
ax.set_title(tytul_wykresu, fontsize=12, fontweight='bold')
ax.set_xlabel("Oś X")
ax.set_ylabel("Oś Y")
ax.set_ylim(min(y_wielkie) - 0.5, max(y_wielkie) + 0.5)
ax.legend(loc="upper left", framealpha=0.9)

ax_info.axis('off')
tekst_info = ax_info.text(0.05, 0.1, "", fontsize=11, family='monospace',
                          bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f5f5", edgecolor="#cccccc", alpha=1.0))

# =============================================================================
# --- SYSTEM OBSŁUGI ZDARZEŃ KLAWIATURY ---
# =============================================================================
stan = {"pauza": False}

def obsluga_klawiatury(event):
    if event.key in [' ', 'enter']: 
        if stan["pauza"]:
            stan["pauza"] = False
            print("[INFO] Wznowiono animację.")
    elif event.key == 's': 
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nazwa_png = f"stopklatka_{timestamp}.png"
        fig.savefig(nazwa_png, bbox_inches='tight')
        print(f"[ZAPIS] Pomyślnie zapisano kadr z panelem jako: {nazwa_png}")

fig.canvas.mpl_connect('key_press_event', obsluga_klawiatury)

print("\n=====================================================================")
print("  ANIMACJA URUCHOMIONA - STEROWANIE WYŁĄCZNIE W OKNIE WYKRESU:")
print("---------------------------------------------------------------------")
print("  • Przy zatrzymaniu w ekstremum: naciśnij SPACJĘ lub ENTER na wykresie.")
print("  • Zapis idealnego kadru (.png wraz z opisem): naciśnij klawisz 'S'.")
print("  • Zamknięcie okna wykresu krzyżykiem kończy sesję i wyzwala zapis wideo.")
print("=====================================================================\n")

# 4. INTERAKTYWNA PĘTLA ANIMACJI
liczba_klatek = 120
klatki = np.arange(liczba_klatek + 1)
ekstremum_zatrzymane = False 

while plt.fignum_exists(fig.number):
    for i in klatki:
        if not plt.fignum_exists(fig.number):
            break
            
        x0 = -2.0 + (4.0 * i / liczba_klatek)
        y0 = f_mat(x0)
        pochodna = fp_mat(x0)
        
        x_odcinek = np.linspace(x0 - 0.5, x0 + 0.5, 10)
        y_odcinek = pochodna * (x_odcinek - x0) + y0
        
        punkt.set_data([x0], [y0])
        styczna_linia.set_data(x_odcinek, y_odcinek)
        
        jest_ekstremum = np.abs(pochodna) < 0.04
        
        if jest_ekstremum:
            status_ekstremum = "EKSTREMUM / PKT. PRZEGIĘCIA (Pochodna bliska 0)"
        elif pochodna > 0:
            status_ekstremum = "(+) Funkcja rośnie w tym punkcie (Pochodna > 0)"
            ekstremum_zatrzymane = False
        else:
            status_ekstremum = "(-) Funkcja maleje w tym punkcie (Pochodna < 0)"
            ekstremum_zatrzymane = False
            
        tekst_info.set_text(
            f" [Parametry Punktu Ruchomego]\n"
            f"  • Współrzędne:  x₀ = {x0:6.2f} |  f(x₀) = {y0:6.2f}\n"
            f"  • Pochodna 1-go rzędu (nachylenie stycznej) = {pochodna:6.2f}\n"
            f"  • Zachowanie:  {status_ekstremum}"
        )
        
        plt.pause(0.03)
        
        if jest_ekstremum and not ekstremum_zatrzymane:
            stan["pauza"] = True
            tekst_info.set_text(
                f" [Parametry Punktu Ruchomego]\n"
                f"  • Współrzędne:  x₀ = {x0:6.2f} |  f(x₀) = {y0:6.2f}\n"
                f"  • Pochodna 1-go rzędu (nachylenie stycznej) = {pochodna:6.2f}\n"
                f"  • Zachowanie:  {status_ekstremum}\n"
                f"  Wciśnij SPACJĘ/ENTER by wznowić. 'S' by zapisać PNG."
            )
            plt.draw()
            
            while stan["pauza"] and plt.fignum_exists(fig.number):
                plt.pause(0.05)
                
            ekstremum_zatrzymane = True

    ekstremum_zatrzymane = False

# Zamknięcie okna interaktywnego
plt.ioff()
plt.close('all')

# =============================================================================
# --- IZOLOWANY, NIE-OKIENKOWY EKSPORT (KLUCZOWE PRZEŁĄCZENIE SILNIKA) ---
# =============================================================================
if decyzja_gif == "t" or decyzja_mp4 == "t":
    print("\n[EKSPORT] Przełączanie systemu graficznego w tryb 'Agg' (Headless)...")
    
    # !!! KLUCZOWA LINIA: Całkowite odcięcie Matplotlib od menedżera okien systemowych/Spydera !!!
    plt.switch_backend('Agg')
    from matplotlib.animation import FuncAnimation
    
    # Budujemy strukturę wykresu w czystej pamięci RAM
    fig_save, (ax_s, ax_i) = plt.subplots(2, 1, figsize=(9, 8), gridspec_kw={'height_ratios': [3, 1]})
    fig_save.subplots_adjust(hspace=0.3)
    
    ax_s.plot(x_wielkie, y_wielkie, color=kolor_wykresu, linewidth=2.5, label=wzor_tekst)
    punkt_s, = ax_s.plot([], [], 'ro', markersize=8, label="Bieżący punkt (x₀, f(x₀))")
    styczna_s, = ax_s.plot([], [], color=kolor_stycznej, linestyle=styl_stycznej, linewidth=1.5, label="Styczna w x₀")
    
    ax_s.axhline(0, color='black', linewidth=0.8, linestyle=':')
    ax_s.axvline(0, color='black', linewidth=0.8, linestyle=':')
    ax_s.grid(True, linestyle=':', alpha=0.5)
    ax_s.set_title(tytul_wykresu, fontsize=12, fontweight='bold')
    ax_s.set_xlabel("Oś X")
    ax_s.set_ylabel("Oś Y")
    ax_s.set_ylim(min(y_wielkie) - 0.5, max(y_wielkie) + 0.5)
    ax_s.legend(loc="upper left")
    
    ax_i.axis('off')
    tekst_s = ax_i.text(0.05, 0.1, "", fontsize=11, family='monospace',
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="#f5f5f5", edgecolor="#cccccc", alpha=1.0))
    
    klatki_eksportu = np.linspace(-2.0, 2.0, 120)
    
    def update_zapis(frame_x0):
        y0 = f_mat(frame_x0)
        pochodna = fp_mat(frame_x0)
        x_odcinek = np.linspace(frame_x0 - 0.5, frame_x0 + 0.5, 10)
        y_odcinek = pochodna * (x_odcinek - frame_x0) + y0
        
        punkt_s.set_data([frame_x0], [y0])
        styczna_s.set_data(x_odcinek, y_odcinek)
        
        if np.abs(pochodna) < 0.04:
            status = "EKSTREMUM / PKT. PRZEGIĘCIA (Pochodna bliska 0)"
        elif pochodna > 0:
            status = "(+) Funkcja rośnie w tym punkcie (Pochodna > 0)"
        else:
            status = "(-) Funkcja maleje w tym punkcie (Pochodna < 0)"
            
        tekst_s.set_text(
            f" [Parametry Punktu Ruchomego]\n"
            f"  • Współrzędne:  x₀ = {frame_x0:6.2f} |  f(x₀) = {y0:6.2f}\n"
            f"  • Pochodna 1-go rzędu (nachylenie stycznej) = {pochodna:6.2f}\n"
            f"  • Zachowanie:  {status}"
        )
        return punkt_s, styczna_s, tekst_s

    animacja_eksport = FuncAnimation(fig_save, update_zapis, frames=klatki_eksportu, blit=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    if decyzja_gif == "t":
        filename_gif = f"animacja_pochodne_{timestamp}.gif"
        print(f" -> Zapisuję GIF: {filename_gif} ... ", end="")
        sys.stdout.flush()
        try:
            animacja_eksport.save(filename_gif, writer="pillow", fps=25)
            print("Zakończono pomyślnie!")
        except Exception as e:
            print(f"\n[BŁĄD ZAPISU GIF]: {e}")

    if decyzja_mp4 == "t":
        filename_mp4 = f"animacja_pochodne_{timestamp}.mp4"
        print(f" -> Zapisuję MP4: {filename_mp4} ... ", end="")
        sys.stdout.flush()
        try:
            animacja_eksport.save(filename_mp4, writer="ffmpeg", fps=25)
            print("Zakończono pomyślnie!")
        except Exception as e:
            print(f"\n[BŁĄD ZAPISU MP4]: {e}")

    plt.close(fig_save)

print("\nProgram zakończył pracę pomyślnie. Do zobaczenia!")
os._exit(0)