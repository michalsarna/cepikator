#!/usr/bin/env python3

import requests
import urllib3
import argparse
import json
import os
from tqdm import tqdm
import zipfile
import logging
import datetime

def getJsonFromCEPIK(url):
  response = requests.get(url, verify=False)
  return response.text.rstrip()

def getJsonFromFile(filename):
  with open(filename, "r") as read_file:
    return read_file.read().rstrip()

def createDirecotry(path):
  if ( os.path.exists(path) == False):
    try:
      os.mkdir(path)
    except OSError:
      logging.error("Creation of the directory %s failed" % path)
    else:
      logging.info("Successfully created the directory %s " % path)

def getZipsFromCEPIK(fileList, downloadPath, forceDownload, unzip, unzipPath):
  createDirecotry(downloadPath)  
  for fileName in tqdm(fileList, desc="files processed"):
    fileWithPath = downloadPath+"/"+fileName
    logging.info("Downloading file %s" % str(fileWithPath))
    t=tqdm()
    if (os.path.exists(fileWithPath) == False or forceDownload == True):
      with requests.get(fileList[fileName], stream=True, verify=False) as r:
        total_size = int(r.headers.get("content-length", 0))
        t=tqdm(total=total_size, unit="iB", unit_scale=True, desc=fileName)
        r.raise_for_status()
        with open(fileWithPath, "wb") as f:
          for chunk in r.iter_content(chunk_size=8192): 
            if chunk: 
              t.update(len(chunk))
              f.write(chunk)
    else:
      t.display("File already exists")
      logging.info("File already exists")
    if (unzip == False):
      createDirecotry(unzipPath)
      with zipfile.ZipFile(fileWithPath, 'r') as zip_ref:
        logging.info("Extracting file %s" % str(fileWithPath))
        t.display("Extracting file: %s" % fileName)
        zip_ref.extractall(unzipPath)
        t.display("done")

def main(args):
  #print("args:", args)
  if (args.logfile == None):
    defaultLogsDirectory = "./logs"
    defaultFullName = defaultLogsDirectory+"/pobieraczek-"+str(datetime.date.today())+".log"
    if (not os.path.exists(defaultLogsDirectory)):
      os.mkdir(defaultLogsDirectory)
    args.logfile = defaultFullName
  logging.basicConfig(filename=args.logfile,level=logging.INFO)
  logging.info("start: %s" % str(datetime.datetime.now()))
  logging.info("ARGS: %s" %str(args))
  urllib3.disable_warnings()
  url = "https://api.cepik.gov.pl/pliki"
  downloadDirectory = "./download"
  csvDirectory = "./source_csv"
  if (args.testFile == None ):
    returned = getJsonFromCEPIK(url)
    logging.info("Getting source info from local file")
  else:
    returned = getJsonFromFile(args.testFile)
    logging.info("Getting source info from CEPiK api.")
  loaded = json.loads(returned)
  data = loaded["data"]
  fileList = {}
  for d in data:
    fileList[str(d["id"]+"_"+d["attributes"]["data-utworzenia-pliku"]+".zip")] = d["attributes"]["url-do-pliku"]
  getZipsFromCEPIK(fileList, downloadDirectory, args.forceDownload, args.unzip, csvDirectory)
  logging.info("stop: %s" % str(datetime.datetime.now()))

################################## MAIN FUNCTION ##################################

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--test-file", action="store", dest="testFile", help="file to use insted of ")
  parser.add_argument("--no-unzip", action="store_true", default=False, dest="unzip", help="perform unzipping")
  parser.add_argument("--force-download", action="store_true", default=False, dest="forceDownload", help="force download and overwrite files")
  parser.add_argument("-lf", "--logfile", help="Allows to use different logfile to use", action="store", default=None)
  args = parser.parse_args()
  main(args)