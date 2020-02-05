# CEPiKaTOR - Statystyki CEPiK dla wytrwałych.

Celem tego projektu jest maksymalne ułatwienie pobrania danych (szczególnie archiwalnych) z CEPiK. 
Niestety API CEPiK nie pozwala na składanie zapytań dot. ojazdów starszych ni 2 lata.
```
 "error-result": "Przepraszamy, nie można zwrócić danych.",
 "error-reason": "Parametry: data-od, data-do mają nieprawidłową wartość.
 Błędny zakres dat. Maksymalny zakres lat to: 2.",
```
Dlatego tez powastał cepikator - czyli zbiór skryptów, które mają na celu ułatwienie procesu pobierania danych (w postaci plików CSV) i ładowania ich do bazy danych. 

Oficjalna dokumentacja API CEPiK dostepna jest [TU](https://api.cepik.gov.pl/doc).
## Lista plików:
 - pobieraczek.py -  pobiera pliki z danymi pojazdów z CEPiK i rozpakowuje je.
 - csvToDB.py - exportuje pliki CSV pobrane z CEPiK do wybranego typu bazy danych.
 - INSTALL.md - opis wymagań dot. systemu i mniej więcej jak to zainstalowac

***
#####Uwaga: 
Uzywasz na własne ryzyko.