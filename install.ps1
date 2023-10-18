
python.exe -m venv venv
venv//Scripts//Activate.ps1
python.exe -m pip install --upgrade pip
pip3.exe install -r requirements.txt
flask db init
flask db migrate -m "create all"
flask db upgrade
python.exe install.py

$username = "admin"
$password = "0000"

echo "administrator credentials", "username : $username", "password : $password" | Format-Table