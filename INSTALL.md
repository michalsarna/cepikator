
# Instalacja i konfiguracja

#### Wymagania:
Aby uzywacepikatora musisz miec zainstalowanego Pythona 3 oraz Pip. Osobiscie zalecam uzywanie virtualnych środowisk z pythonem, ale to ju jak kto lubi ;)

#### Instalacja:
- w środowisku wirtualnym:
```
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
```
No i gotowe. Teraz mozna zaczynac. 
***
####For Mac OS X users that have installed Mongo or MySQL from brew.: 
***
## Mongo
- For Mac OS X: 

  To have launchd start mongodb/brew/mongodb-community now and restart at login:
  ```bash
  brew services start mongodb/brew/mongodb-community
  ```

  Or, if you don't want/need a background service you can just run:
  ```bash
  mongod --config /usr/local/etc/mongod.conf
  ```
## MySQL
- For Mac OS X: 

  MySQL is configured to only allow connections from localhost by default.

  To have launchd start mysql now and restart at login:
  ```
  brew services start mysql
  ```
  Or, if you don't want/need a background service you can just run:
  ```
  mysql.server start
  ```
  To connect run:
  ```
  mysql -uroot
  ```
