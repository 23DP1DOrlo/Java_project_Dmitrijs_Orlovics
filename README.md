## Cube Timer lietojumprogramma

## Apraksts

Šī lietojumprogramma ir izstrādāta, lai sekotu līdzi laikam, kas nepieciešams Rubika kuba atrisināšanai. Tā nodrošina taimeri, kas seko līdzi risināšanas laikam, un tai ir arī funkcionalitāte solve sesiju apstrādei, ieskaitot rezultātu filtrēšanu un šķirošanu, kā arī iespēju dzēst un saglabāt datus.

Turklāt lietojumprogramma atbalsta autentifikācijas sistēmu, kas ļauj lietotājam pieteikties savā kontā, lai saglabātu savas salikšanas sesijas un vēlāk tās apskatītu.

---

## Funkcijas

- **Taimeris**:
    - Palaižās un apstājās ar atstarpes taustiņu.
    - Atbalsta sekundes un sekundes simtdaļas.
    - Paziņojumi lietotājam ar informāciju par pašreizējo stāvokli.
  
- **Sesijas**:
    - Katras sesijas laika ierakstīšana un parādīšana ekrānā.
    - Iespēja šķirot un filtrēt rezultātus pēc laika.
    - Vidējo vērtību rādīšana (AO5 un AO12).
    - Solve dzēšana.
  
- **Autentifikācija**:
    - Lietotāja pieslēsšana un reģistrācija.
    - Katrs lietotājs var saglabāt savus risinājuma datus atsevišķā failā.

---

## Instalēšana

#### Prasības

Lai palaistu lietojumprogrammu, ir jābūt instalētam Python un nepieciešamajām bibliotēkām.


1. Instalējiet Python (ja tas vēl nav instalēts):
   - Lejupielādējiet Python no oficiālās vietnes: https://www.python.org/.
   - Pārliecinieties, ka Python ir pievienots PATH.

2. Instalējiet nepieciešamās bibliotēkas:
   ````bash
   pip install PyQt5

3. Pārliecinieties, ka jums ir failu struktūra datu saglabāšanai, piemēram, mape ```Data``, kurā saglabāt rezultātus JSON formātā.

---

## Projekta struktūra

Programma sastāv no vairākiem moduļiem:

- **``timer_window.py`**: Galvenā taimera loga klase, kas pārvalda laiku un montāžas sesijas.
- **`auth.py`**: Modulis lietotāju autentifikācijai (pieteikšanās un reģistrācija).
- **`scramble_generator.py`**: Rubika kuba nejaušības kodu ģenerators.
- **`login_window.py`**: Logs pieteikšanās un jauna lietotāja reģistrēšanai.

---

#### Funkcionalitāte


### 1. Pieteikšanās

Pēc lietojumprogrammas palaišanas tiek parādīts pieteikšanās logs ar laukiem, kuros jāievada **logins** un **parole**.

- Ja jums jau ir konts, ievadiet savu lietotājvārdu un paroli un pēc tam noklikšķiniet uz pogas **Pieslēgties**.
- Ja neesat reģistrējies, noklikšķiniet uz pogas **Reģistrēties**, lai izveidotu jaunu kontu.

Pēc veiksmīgas pieteikšanās tiks atvērts galvenais taimera logs.



### 2. Taimeris

Pēc pieslēgšanas tiks parādīts taimera logs, kurā tiek uzskaitīts laiks, kas nepieciešams, lai atrisinātu Rubika kubu. Taimeris darbojas šādi:

- Lai palaistu jaunu taimeri, turiet nospiestu **Space** (atstarpes taustiņu) **0,5 sekundes**.
- Atlaižot viņu, taimeris tiks iedarbināts, un jūs varēsiet salikt kubu.
- Kad esat pabeidzis darbu, nospiediet taustiņu **Space**, un taimeris apstāsies. Rezultāts tiks saglabāts jūsu sesijā.

### 3. Rezultāti

Loga apakšdaļā ir redzami jūsu veidošanas rezultāti. Jūs varat:

- **Izdzēst atlasīto solve'u**, noklikšķinot uz tās ar peles labo pogu un nospiežot **Delete** pogu.
- **Filtrēt** vai **Sortēt** solve'us pēc laika, izmantojot minimālā un maksimālā laika ievades laukus un šķirošanas pogas.
- **Vidējie rādītāji** AO5 (vidējais rādītājs no pēdējiem 5 solve'iem, izņemot labāko un sliktāko) un AO12 (vidējais rādītājs no pēdējām 12 solve'iem).

### 4. Rezultātu saglabāšana
Rezultāti tiek saglabāti **JSON failā** (`Data/solves.json`) un tiek reģistrēti katru reizi:

- Lietotājvārds.
- Scramble (nejauša kombinācija kā samaisīt kubu).
- Risinājuma laiks.
- Ieraksta laiks.

---

## Lietošanas piemērs

1. Palaidiet lietojumprogrammu.
2. Ievadiet savu lietotājvārdu un paroli, lai pieteiktos.
3. Turiet **Space** (atstarpe) 0.5s un atlaidat, lai sāktu mērīt laiku.
4. Atrisiniet kubu un nospiediet **Space** tik ātri kā varat, lai apturētu taimeri.
5. Rezultāts tiks pievienots sesiju sarakstam.
6. Izmantojiet filtrēšanu un šķirošanu, lai redzētu vēlamos datus.

---
