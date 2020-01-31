#!/usr/bin/env python3

import argparse
import os
import csv
import json
import pymongo
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
import mysql.connector
import logging
import datetime


def main(args):
  #print("args: ", args)
  if (args.logfile == None):
    defaultLogsDirectory = "./logs"
    defaultFullName = defaultLogsDirectory+"/csvToDB-"+str(datetime.date.today())+".log"
    if (not os.path.exists(defaultLogsDirectory)):
      os.mkdir(defaultLogsDirectory)
    args.logfile = defaultFullName
  logging.basicConfig(filename=args.logfile,level=logging.INFO)
  logging.info("start: "+str(datetime.datetime.now()))
  logging.info("ARGS: "+str(args))
  fileList = []
  if (args.file != None):
    fileList.append(args.file)
  else:
    for file in os.listdir(args.directory):
      fileList.append(os.path.join(args.directory, file))
  if (args.useMysql == False):
    logging.info("Using Mongo")
    insertIntoMongo(args, fileList)
  else:
    args.dbPort = 3306
    args.dbUser = "cepikator"
    args.dbPass = "<c3p1katOr>"
    logging.info("Using Mysql")
    insertIntoMySql(args, fileList)
  logging.info("stop: "+str(datetime.datetime.now()))

def insertIntoMongo(args, fileList):
  if (args.dbPass != "" and args.dbUser != ""):
    dbUrl = "mongodb://"+str(args.dbUrl)+":"+str(args.dbPass)+"@"+str(args.dbHost)+":"+str(args.dbPort)+"/cepikator"
  else:
    dbUrl = "mongodb://"+str(args.dbHost)+":"+str(args.dbPort)+"/cepikator"
  client = pymongo.MongoClient(dbUrl)
  db = client.cepikator
  for cfile in tqdm(fileList, desc="Files processed", unit_scale=False, unit=""):
    fileLineCount = sum(1 for line in open(cfile))
    with open(cfile, newline='') as csvfile:
      csvfile = csv.DictReader(csvfile, delimiter=',')
      for row in tqdm(csvfile, total=fileLineCount ,desc=cfile, unit='Lines',unit_scale=True):
        try:
          db.pojazdy.insert_one(row)
        except pymongo.errors.DuplicateKeyError as e:
          logging.info("skipped pojazd_id: %s", row.get('pojazd_id'))
          pass

def insertIntoMySql(args, fileList):
  config = {
    'user': args.dbUser,
    'password': args.dbPass,
    'host': args.dbHost,
    'database': 'cepikator',
    'raise_on_warnings': True
  }
  cnx = mysql.connector.connect(**config)
  cursor = cnx.cursor()
  add_pojazdy = ("INSERT INTO pojazdy "
    "(pojazd_id, marka, kategoria, typ, model, wariant, wersja, rodzaj, podrodzaj, przeznaczenie, pochodzenie, rodzaj_tab_znamionowej, rok_produkcji, sposob_produkcji, data_pierwszej_rej, data_rejestracji_ost, data_pierwszej_rej_za_granica, pojemnosc_silnika, moc_do_masy, moc_silnika, moc_silnika_hybrydowego, masa_wlasna, masa_pgj, dopuszczalna_masa_calkowita, maksymalna_masa_calkowita, dopuszczalna_ladownosc_calk, maksymalna_ladownosc_calk, dopuszczalna_masa_ciag_zesp, liczba_osi, naj_dopuszczalny_nacisk_osi, naj_maksymalny_nacisk_osi, max_masa_przyczepy_z_hamulcem, max_masa_przyczepy_bez_ham, liczba_miejsc_ogolem, liczba_miejsc_siedzacych, liczba_miejsc_stojacych, rodzaj_paliwa, rodzaj_paliwa_alternatywnego, rodzaj_paliwa_alternatywnego2, sr_zuzycie_pal, rodzaj_zawieszenia, radar, hak, kierownica_polozenie, kierownica_z_prawej, katalizator, producent_podstawowy, kod_ident, rozstaw_osi_kierowanej, rozstaw_kol_max, rozstaw_kol_sred, rozstaw_kol_min, emisja_co2_redukcja, wersja_rpp, kod_rpp, data_wyrejestrowania, przyczyna_wyrejestrowania, data_wprowadzenia_danych, akt_miejsce_rej_wojwe, akt_miejsce_rej_powiat, akt_miejsce_rej_gmina, siedziba_wlasciciela_woj, siedziba_wlasciciela_pow, siedziba_wlasciciela_gmina, data_pierwszej_rej_w_kraju, createtimestamp, modifytimestamp, siedziba_wlasciciela_woj_teryt, akt_miejsce_rej_wojew_teryt, emisja_co2, emisja_co2_pal_alternatywne1) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  )
  for cfile in tqdm(fileList, desc="Files processed", unit_scale=False, unit=""):
    fileLineCount = sum(1 for line in open(cfile))
    with open(cfile, newline='') as csvfile:
      csvfile = csv.reader(csvfile, delimiter=',')
      header = next(csvfile)
      for row in tqdm(csvfile, total=fileLineCount ,desc=cfile, unit='Lines',unit_scale=True):
        if header != None:
          new_row = []
          for value in row:
            if value == '':
              new_row.append(None)
            else:
              new_row.append(value)
          try:
            cursor.execute(add_pojazdy, new_row)
          except mysql.connector.Error as err:
            logging.info("Something went wrong: {}".format(err))
          cnx.commit()
  cursor.close()
  cnx.close()
        

################################## MAIN FUNCTION ##################################

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-f", "--file", action="store", dest="file", help="file to use insted of all files in source_csv directory")
  parser.add_argument("-d", "--directory", action="store", dest="directory", default="./source_csv",help="directory to use insted of source_csv directory")
  parser.add_argument("--use-mysql", action="store_true", default=False, dest="useMysql", help="Change DB type from Mongo to MySQL/MariaDB.")
  parser.add_argument("--db-host", action="store", default="127.0.0.1", dest="dbHost", help="Database address to use. (default: 127.0.0.1)")
  parser.add_argument("--db-port", action="store", default="27017", dest="dbPort", help="Database port to use. (default: 27017 for mongo and 3306 for MySQL/MariaDB)")
  parser.add_argument("--db-user", action="store", default="", dest="dbUser", help="Database user to use. (default: \"\")")
  parser.add_argument("--db-pass", action="store", default="", dest="dbPass", help="Database users password to use. (default: \"\")")
  parser.add_argument("-lf", "--logfile", help="Allows to use different logfile to use", action="store", default=None)
  args = parser.parse_args()
  main(args)