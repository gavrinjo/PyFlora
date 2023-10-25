# pyFlora

Algebra Python Developer

## Instalation

First of all, it is necessary to create a new **VIRTUAL ENVIROMET** in the app root folder and activate it.

```ps
python.exe -m venv venv
```
```ps
venv/scripts/activate.ps1
```
In case scripts cannot be executed in PowerShell, it is necessary to set **ExecutionPolicy** to **Unrestricted**

```ps
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope LocalMachine
```
After that, it is necessary to install the required packages
```ps
pip install -r requirements.txt
```

- ### Test mail server

The application includes an email component, **sending messages** and **password reset via email**

before starting the mail server, it is necessary to set the environment variables as follows.

```ps
# through the powershell terminal
$env:MAIL_SERVER=localhost
$env:MAIL_PORT=8025

# through the .env file (located in the root folder of the application)
MAIL_SERVER=localhost
MAIL_PORT=8025
```

Python comes with the SMTPD component, and in order to start the test mail server, you need to run the following command in a separate PowerShell instance.

```ps
python -m smtpd -n -c DebuggingServer localhost:8025
```

- ### Weather

The application also includes a component for **Current weather conditions**

The data is pulled from the [OpenWeather](https://openweathermap.org/) page via an **API** key

The API key is set in the environment variable as follows

```ps
# through the powershell terminal
$env:WEATHER_API=api_key

# through the .env file (located in the root folder of the application)
WEATHER_API=api_key
```

## First run

It is not necessary to initialize the database manually <small> *(although it is possible, in that case the database will not be filled with predefined records)* </small> like so

```ps
flask db init
flask db migrate -m "descriptive message"
flask db upgrade
```
Instead, it is enough to start the application and at the first run the database will be created and filled with predefined records.

```ps
flask run
  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
After terminating the launched application, it is advised to perform a database migration and upgrade.

```ps
flask db migrate -m "descriptive message"
flask db upgrade
```
Do this every time changes are made to `db models`.

## Authorization

User authorization, ***login, logout, registration, password reset*** are implemented in the application

At first run, an administrative account is created with the login details below

```
username: admin
password: 0000
```
The administrative user has the right to access the admin portal within the application and access to all users and models

The administrator has the authority to add admin privileges to users


## Measurements

- **salinity** (reading from the sensor) %
- **reaction** (reading from the sensor) pH
- **humidity** (reading from the sensor) %
- **temperature** (reading from the meteo station via API) &deg;C
- **sunlight** (reading from the sensor) lux
- **nutrient** (reading from the sensor) %

## Charts

Python package Plotly was used for the charts

- Line chart
- Histogram chart
- Pie chart (radar chart is a better option, but it is not integrated)

## References

- Each predefined plant in the db has a reference on Wikipedia and vrtlaric.hr
- [Indicator value](https://en.wikipedia.org/wiki/Indicator_value) used as a base for measured values and a scale
- [FloraVeg](https://floraveg.eu/download/) Indicator Value database
- [Vrtlarica.hr](https://www.vrtlarica.hr/) the largest encyclopedia on gardening in Croatia