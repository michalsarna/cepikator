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

def getZipFromCEPIK(fileName, fileURL, path):
  if ( os.path.exists(path) == False):
    try:
      os.mkdir(path)
    except OSError:
      print ("Creation of the directory %s failed" % path)
    else:
      print ("Successfully created the directory %s " % path)
  #print("\nDownloading from url: " + fileURL + "\n")
  with requests.get(fileURL, stream=True, verify=False) as r:
    total_size = int(r.headers.get("content-length", 0))
    t=tqdm(total=total_size, unit="iB", unit_scale=True, desc=fileName)
    r.raise_for_status()
    with open(path+"/"+fileName, "wb") as f:
      for chunk in r.iter_content(chunk_size=8192): 
        if chunk: 
          t.update(len(chunk))
          f.write(chunk)

def getZipFileList(path):
  zipFileList = []
  for file in os.listdir(path):
    if file.endswith(".zip"):
        zipFileList.append(os.path.join(path, file))
  return zipFileList

def unzipFiles(sourceDirectory, destinationDirectory):
  if ( os.path.exists(destinationDirectory) == False):
    try:
      os.mkdir(destinationDirectory)
    except OSError:
      print ("Creation of the directory %s failed" % destinationDirectory)
    else:
      print ("Successfully created the directory %s " % destinationDirectory)
  zipFileList = getZipFileList(sourceDirectory)
  for file in zipFileList:
    #print(zipFileList)
    with zipfile.ZipFile(file, 'r') as zip_ref:
      print("Extracting file: %s" % file)
      zip_ref.extractall(destinationDirectory)
      print("... done.")
      os.unlink(file)

def main(args):
  #print("args:", args.testFile)
  urllib3.disable_warnings()
  url = "https://api.cepik.gov.pl/pliki"
  downloadDirectory = "./download"
  csvDirectory = "./source_csv"
  if (args.omit == False):
    if (args.testFile == None ):
      returned = getJsonFromCEPIK(url)
    else:
      returned = getJsonFromFile(args.testFile)
    loaded = json.loads(returned)
    data = loaded["data"]
    fileList = {}
    for d in data:
      fileList[str(d["id"]+"_"+d["attributes"]["data-utworzenia-pliku"]+".zip")] = d["attributes"]["url-do-pliku"]
    for f in fileList:
      getZipFromCEPIK(f, fileList[f], downloadDirectory)
  if (args.unzip == True):
      unzipFiles(downloadDirectory, csvDirectory)
      

################################## MAIN FUNCTION ##################################

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--test-file", action="store", dest="testFile", help="file to use insted of ")
  parser.add_argument("--omit-download", action="store_true", default=False, dest="omit", help="omit download")
  parser.add_argument("--no-unzip", action="store_true", default=True, dest="unzip", help="perform unzipping")
  args = parser.parse_args()
  main(args)