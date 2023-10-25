# pyFlora

Seminarski rad Algebra Python Developer

## Instalation

Prije svega potrebno je u mapi gdje se nalazi web aplikacija napraviti novi **VIRTUAL ENVIROMET** te isti aktivirati.

```ps
python.exe -m venv venv
```
```ps
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

## Prvo pokretanje

Nije potrebno ručno raditi inicijalizaciju baze <small> *(iako je moguće, u tom slućaju baza neće biti popunjena sa predefiniranim stavkam)* </small>

```ps
flask db init
flask db migrate -m "opisna poruka"
flask db upgrade
```
Dovoljno je smo pokrenuti aplikaciju i pri prvom startanju će se napraviti baza i popuniti s predefiniranim stavkama.

```ps
flask run
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
Nakon terminiranja pokrenute aplikacije, može se napraviti migracija i upgrade.

```ps
flask db migrate -m "opisna poruka"
flask db upgrade
```

## Testni mail server

U aplikaciju je uključena email komponenta, **slanje poruka** i **resetiranje passworda putem maila**

prije pokretanja mail servera potrebno je postaviti environment varijable na sljledeći način.

```ps
# kroz powershell terminal
$env:MAIL_SERVER=localhost
$env:MAIL_PORT=8025

# kroz .env datoteku (nalazi se u root folderu aplikacije)
MAIL_SERVER=localhost
MAIL_PORT=8025
```

Python dolazi s SMTPD komponentom, te da bi pokrenuli testni mail server potrebno je u zasebnoj PowerShell instanci pokrenuti sljedeću komandu.

```ps
python -m smtpd -n -c DebuggingServer localhost:8025
```

## Vremenska prognoza

Također u aplikaciju je uključena i komponenta za **Trenutne vremenske uvijete**

Podaci se povlaće s stranice [OpenWeather](https://openweathermap.org/) putem **API** ključa

API kljuć se postavlja u environment varijable na sljedeći način

```ps
# kroz powershell terminal
$env:WEATHER_API=api_kljuc

# kroz .env datoteku (nalazi se u root folderu aplikacije)
WEATHER_API=api_kljuc
```


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