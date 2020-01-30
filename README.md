# CEPiKaTOR

## File list:
 - pobieraczek.py -  pobera dane pojazdów z CEPiK
 - csvToDB.py - exportuje pliki csv pobrane z CEPiK do Bazy danych
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
