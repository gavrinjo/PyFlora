# pyFlora

Seminarski rad Algebra Python Developer

---

## Instalation

Prije svega potrebno je u mapi gdje se nalazi web aplikacija napraviti novi **VIRTUAL ENVIROMET** te isti aktivirati.


```{code}ps
:filename: test.bla
:name: my-program
:caption: Creating a TensorMesh using SimPEG
python.exe -m venv venv
venv/scripts/activate.ps1
```
U slučaju da se skripte ne mogu izvršavati u PowerShelu, potrebno je postaviti **ExecutionPolicy** na **Unrestricted**

```ps
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope LocalMachine
```
Nakon toga potrebno je instalirati potrebne pakete
```ps
pip install -r requirements.txt
````



## Line chart

- raspon od 20 mjerenja unatrag
- x - datumi mjerenja
- y - izmjerene vrijednosti
- za svaki senzor posebna linija + temperatura za svako mjerenje
- markeri (opcionalno)
- legenda
- nazivi osi
- naslov

## Histogram chart

- u obzir uzima sva mjerenja
- uzima vrijednost mjerenja i raspon od min do max vrijednosti skale
- legenda
- nazivi osi
- naslov

## Pie chart (radar chart je bolja opcija)

- koristi za usporedbu neutralne vrijednosti i zadnje mjerenje

## mjerenja koja će se koristiti

- salinitet (očitanje sa senzor)
- pH vrijednost (očitanje sa senzora)
- vlaga (očitanje sa senzora)
- temperatura (očitanje sa meteo stanice putem API-a)

## weather template

- <https://www.themezy.com/demos/128-steel-weather-free-responsive-website-template>

## Weather API

- <https://open-meteo.com/en/docs#latitude=45.8144&longitude=15.978>
  

## reference

- dodati reference na vanjski sadržaj (link na wikipediju ili vrtlarica.hr)