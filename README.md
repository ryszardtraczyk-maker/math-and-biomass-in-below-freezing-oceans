# Pakiet Programów Matematycznych, Fizycznych i Biologicznych (Python / EXE)

Wytworzony zestaw autorskich aplikacji służy do zaawansowanej wizualizacji 3D pojęć matematycznych, analizy ciągłości funkcji, modelowania stycznych oraz symulacji ekologicznych w środowiskach polarnych i kosmicznych. 

## Jak uruchomić programy?
1. **Kod źródłowy:** Pliki źródłowe z rozszerzeniem *.py* znajdują się na liście plików powyżej.
2. **Wersje wykonywalne (Wersje instalacyjne):** Gotowe pliki *.exe* (dla systemu Windows) można pobrać, klikając sekcję **Releases** znajdującą się po prawej stronie ekranu. 
*Wskazówka: Programy posiadają domyślne parametry. Aby szybko przetestować ich działanie, wystarczy akceptować sugerowane wartości klawiszem Enter.*

---

## Spis i opis programów

### 1. Wizualizacja ciągów Cauchy'ego w 3D
* **Pliki:** ciagi_Couchy10a.exe / ciagi_Couchy10a.py
* **Opis:** Program wizualizuje przestrzenną definicję warunku Cauchy’ego: ∀ε > 0 ∃j ∈ N ∀a,b ∈ N: a,b ≥ j ⇒ d(xₐ, x_b) < ε. Aplikacja animuje w przestrzeni 3D przechodzenie kolejnych wyrazów ciągu do kuli o zadanym promieniu ε oraz wybór odległości d(xₐ, x_b), dla której zachodzi ten warunek dla wszystkich wskaźników większych bądź równych j.
* **Eksport:** Zapis animacji do formatów GIF oraz MP4.

### 2. Animacja różniczki zupełnej i nieciągłości powierzchni
* **Pliki:** Rozniczka_zupelna_animacja21.exe / Rozniczka_zupelna_animacja21.py
* **Opis:** Program pokazuje kontrprzykład dla założenia, że funkcja zbudowana z podstawowych operacji na funkcjach ciągłych (wielomiany, trygonometria) jest automatycznie ciągła w całej dziedzinie. Wizualizuje iloraz dwóch płaszczyzn tworzący fuzję w powierzchnię, która posiada pochodne cząstkowe w punkcie (0,0) równe 0 (ciągłość wzdłuż osi X oraz Y), lecz na skosie posiada granicę równą ½. Przenikanie geometryczne (rogi płaszczyzn składowych ciągnące w przeciwne strony) obrazuje mechanizm rozdarcia i nieciągłości w punkcie (0,0) pomimo istnienia różniczek cząstkowych.
* **Funkcje dodatkowe:** Wybór kąta patrzenia i obrotu wokół osi 0Z. Zapis animacji do GIF oraz MP4.

### 3. Animacja przebiegu stycznej dla 8 funkcji
* **Pliki:** wykresy_all8.exe / wykresy_all8.py
* **Opis:** Aplikacja prezentuje dynamiczny przebieg stycznej dla 8 wbudowanych funkcji z możliwością zdefiniowania własnego wzoru (program wyświetla instrukcję poprawnego wpisu składni języka Python). Program automatycznie wyznacza i wskazuje ekstrema funkcji.
* **Funkcje dodatkowe:** Personalizacja kolorystyki wykresu, edycja tytułów. Zapis wyników do plików GIF oraz MP4.

### 4. Model periodyczny symulacji biomasy podlodowej (Antarktyka & Europa)
* **Pliki:** biomass_animation_periodic_model.exe / biomass_animation_periodic_model.py
* **Opis:** Program do składania funkcji periodycznych w celu symulacji zmian biomasy organizmów żyjących w temperaturach poniżej punktu zamarzania wody. Wykorzystuje historyczne i aktualne dane od 1978 roku z bazy danych CCAMLR online dla prostego łańcucha troficznego (4 poziomy) w Oceanie Antarktycznym, uwzględniając cykle sezonowe oraz anomalie termiczne (lata ciepłe i zimne). Model dokonuje porównania z symulacją warunków podlodowych na księżycu Jowisza – Europie, uwzględniając tamtejsze cykle pozaziemskie.
* **Funkcje dodatkowe:** Pełna dwujęzyczność (Polski / Angielski). Możliwość wprowadzania własnych danych dla obu oceanów. Eksport animacji do GIF/MP4 oraz danych i parametrów do formatów XLSX i DOCX.

### 5. Model liniowo-logistyczny symulacji biomasy podlodowej
* **Pliki:** animation_biomass_linear_5_logistic15.exe / animation_biomass_linear_5_logistic15.py
* **Opis:** Program realizujący analogiczne zadanie symulacji biomasy polaryjnej i egzobiologicznej jak program nr 4, lecz oparty na matematycznym złożeniu modeli logistycznych oraz modelowania liniowego zamiast funkcji ściśle periodycznych.

* Dodatkowe Materiały Naukowe / Supplementary DocumentationDla pełnego zrozumienia biologicznych, fizjologicznych oraz matematycznych podstaw stworzonych symulacji, zachęcamy do zapoznania się z poniższymi szczegółowymi opracowaniami:Model_Biologia.md – Pełna monografia naukowa w języku polskim. Zawiera szczegółową charakterystykę biologiczną i ekologiczną badanych trzech gatunków ryb białokrwistych, unikalne opisy adaptacji korali zimnowodnych, tabele przeliczników biomasy. Model_Biology.md – Full scientific reference material in English. It covers the evolutionary framework of Channichthyidae, thermodynamic and kinetic metabolic systems (Arrhenius, Q10 equations), and structural modeling for permanent sub-ice ecosystems on Jupiter's and Saturn's ice moons (Europa and Enceladus).
