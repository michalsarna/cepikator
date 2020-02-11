## Dropujemy (usuwamy) stara baze i uzytkownika
DROP DATABASE cepikator;
DROP USER 'cepikator'@'localhost';
## Tworzymy bazę danych
CREATE DATABASE cepikator;
## Tworzymy taeblę dla pojazdów
USE cepikator
CREATE TABLE pojazdy ( id INT(20) PRIMARY KEY NOT NULL AUTO_INCREMENT  , pojazd_id BIGINT(40),  marka VARCHAR(30) CHARACTER SET utf8,  kategoria VARCHAR(20) CHARACTER SET utf8,  typ VARCHAR(40) CHARACTER SET utf8,  model VARCHAR(40) CHARACTER SET utf8,  wariant VARCHAR(40) CHARACTER SET utf8,  wersja VARCHAR(40) CHARACTER SET utf8,  rodzaj TEXT CHARACTER SET utf8,  podrodzaj TEXT CHARACTER SET utf8,  przeznaczenie TEXT CHARACTER SET utf8,  pochodzenie TEXT CHARACTER SET utf8,  rodzaj_tab_znamionowej VARCHAR(20) CHARACTER SET utf8,  rok_produkcji VARCHAR(50) CHARACTER SET utf8,  sposob_produkcji VARCHAR(40) CHARACTER SET utf8,  data_pierwszej_rej DATE,  data_rejestracji_ost DATE,  data_pierwszej_rej_za_granica DATE,  pojemnosc_silnika INT(10),  moc_do_masy INT(10),  moc_silnika INT(10),  moc_silnika_hybrydowego INT(10),  masa_wlasna INT(10),  masa_pgj INT(10),  dopuszczalna_masa_calkowita INT(10),  maksymalna_masa_calkowita INT(10),  dopuszczalna_ladownosc_calk INT(10),  maksymalna_ladownosc_calk INT(10),   dopuszczalna_masa_ciag_zesp INT(10),  liczba_osi INT(2),  naj_dopuszczalny_nacisk_osi INT(10),  naj_maksymalny_nacisk_osi INT(10),  max_masa_przyczepy_z_hamulcem INT(10),  max_masa_przyczepy_bez_ham INT(10),  liczba_miejsc_ogolem INT(5),  liczba_miejsc_siedzacych INT(5),  liczba_miejsc_stojacych INT(5),  rodzaj_paliwa VARCHAR(60) CHARACTER SET utf8,  rodzaj_paliwa_alternatywnego TEXT CHARACTER SET utf8,  rodzaj_paliwa_alternatywnego2 VARCHAR(60) CHARACTER SET utf8,  sr_zuzycie_pal VARCHAR(20) CHARACTER SET utf8,  rodzaj_zawieszenia VARCHAR(40) CHARACTER SET utf8,  radar VARCHAR(20) CHARACTER SET utf8,  hak VARCHAR(20) CHARACTER SET utf8,  kierownica_polozenie VARCHAR(20) CHARACTER SET utf8,  kierownica_z_prawej VARCHAR(20) CHARACTER SET utf8,  katalizator VARCHAR(20) CHARACTER SET utf8,  producent_podstawowy VARCHAR(200) CHARACTER SET utf8,  kod_ident VARCHAR(20) CHARACTER SET utf8,  rozstaw_osi_kierowanej VARCHAR(20) CHARACTER SET utf8,  rozstaw_kol_max VARCHAR(20) CHARACTER SET utf8,  rozstaw_kol_sred VARCHAR(20) CHARACTER SET utf8,  rozstaw_kol_min VARCHAR(20) CHARACTER SET utf8,  emisja_co2_redukcja VARCHAR(20) CHARACTER SET utf8,  wersja_rpp VARCHAR(20) CHARACTER SET utf8,  kod_rpp VARCHAR(20) CHARACTER SET utf8,  data_wyrejestrowania DATE,  przyczyna_wyrejestrowania VARCHAR(200) CHARACTER SET utf8,  data_wprowadzenia_danych DATE,  akt_miejsce_rej_wojwe VARCHAR(20) CHARACTER SET utf8,  akt_miejsce_rej_powiat VARCHAR(20) CHARACTER SET utf8,  akt_miejsce_rej_gmina VARCHAR(20) CHARACTER SET utf8,  siedziba_wlasciciela_woj VARCHAR(20) CHARACTER SET utf8,  siedziba_wlasciciela_pow VARCHAR(40) CHARACTER SET utf8,  siedziba_wlasciciela_gmina VARCHAR(40) CHARACTER SET utf8,  data_pierwszej_rej_w_kraju DATE,  createtimestamp DATE,  modifytimestamp DATE,  siedziba_wlasciciela_woj_teryt VARCHAR(20) CHARACTER SET utf8,  akt_miejsce_rej_wojew_teryt VARCHAR(20) CHARACTER SET utf8,  emisja_co2 VARCHAR(20) CHARACTER SET utf8,  emisja_co2_pal_alternatywne1 VARCHAR(20) CHARACTER SET utf8 );
## Dodajemy zytkownika cepikator z hasłem cepikator i dajemy mu wszelkie uprawnienia do bazy cepikator. 
CREATE USER 'cepikator'@'localhost' IDENTIFIED BY '<c3p1katOr>';
GRANT ALL PRIVILEGES ON cepikator.* TO 'cepikator'@'localhost';
FLUSH PRIVILEGES;