
echo "SETTING UP VIRTUAL ENVIRONMENT"
python.exe -m venv venv
echo ""
echo "ACTIVATE VIRTUAL ENVIRONMENT"
venv//Scripts//Activate.ps1
echo ""
echo "UPGRADE PIP PACKAGE MANAGEMENT"
python.exe -m pip install --upgrade pip
echo ""
echo "INSTALLING REQUIRED PACKAGES"
pip3.exe install -r requirements.txt
echo ""
echo "SETTING UP DATATBASE"
flask db init
flask db migrate -m "create all"
flask db upgrade
echo ""
echo "POPULATING DATABASE WITH INITIAL RECORDS"
python.exe install.py

$username = "admin"
$password = "0000"
echo ""
echo "ADMIN LOGIN CREDENTIALS", "USERNAME : $username", "PASSWORD : $password" | Format-Table
start powershell {python -m smtpd -n -c DebuggingServer localhost:8025}
flask run