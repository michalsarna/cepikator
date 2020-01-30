#!/usr/bin/env python3

import requests
import urllib3
import argparse
import json
import os
from tqdm import tqdm
import zipfile

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
      print ("Creation of the directory %s failed" % path)
    else:
      print ("Successfully created the directory %s " % path)

def getZipsFromCEPIK(fileList, downloadPath, forceDownload, unzip, unzipPath):
  createDirecotry(downloadPath)  
  for fileName in tqdm(fileList, desc="files processed"):
    fileWithPath = downloadPath+"/"+fileName
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
    if (unzip == False):
      createDirecotry(unzipPath)
      with zipfile.ZipFile(fileWithPath, 'r') as zip_ref:
        t.display("Extracting file: %s" % fileName)
        zip_ref.extractall(unzipPath)
        t.display("done")

def main(args):
  print("args:", args)
  urllib3.disable_warnings()
  url = "https://api.cepik.gov.pl/pliki"
  downloadDirectory = "./download"
  csvDirectory = "./source_csv"
  if (args.testFile == None ):
    returned = getJsonFromCEPIK(url)
  else:
    returned = getJsonFromFile(args.testFile)
  loaded = json.loads(returned)
  data = loaded["data"]
  fileList = {}
  for d in data:
    fileList[str(d["id"]+"_"+d["attributes"]["data-utworzenia-pliku"]+".zip")] = d["attributes"]["url-do-pliku"]
  getZipsFromCEPIK(fileList, downloadDirectory, args.forceDownload, args.unzip, csvDirectory)

################################## MAIN FUNCTION ##################################

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--test-file", action="store", dest="testFile", help="file to use insted of ")
  parser.add_argument("--no-unzip", action="store_true", default=False, dest="unzip", help="perform unzipping")
  parser.add_argument("--force-download", action="store_true", default=False, dest="forceDownload", help="force download and overwrite files")
  args = parser.parse_args()
  main(args)