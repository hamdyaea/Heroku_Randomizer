#!/usr/bin/env python3

# Developer : Hamdy Abou El Anein
# hamdy.aea@protonmail.com


from flask import Flask, render_template, request
import random
import os
import dropbox
import json
import requests

drkey = os.environ["dropkey"]

# for test only
#drkey = "XXX"


dbx = dropbox.Dropbox(drkey)

filename = "visitors.csv"
countryfile = "countrylist.txt"

def geo():
    global ipcountry
    backadrr = "https://www.ipinfo.io/"
    fulladd = backadrr + str(yourip)

    r = requests.get(fulladd)
    data = r.json()
    ipcountry = data["country"]
    # for test only uncomment
    #ipcountry = "CH"

def up():
    with open(filename, "rb") as f:
        dbx.files_upload(f.read(), "/" + filename)
    
    with open(countryfile, "rb") as f:
        dbx.files_upload(f.read(), "/" + countryfile)

def down():
    dbx.files_download_to_file(filename, "/" + filename)
    dbx.files_download_to_file(countryfile, "/" + countryfile)

def deleter():
    dbx.files_delete("/" + filename)
    dbx.files_delete("/" + countryfile)


def main():
    global counter,country, maxcountry

    down()

    f = open(filename, "r")
    value = f.read()

    counter = int(value) + 1
    
    with open(countryfile) as f:
        country = [line.rstrip() for line in f]
    
    maxcountry = max(set(country), key=country.count)
             
    country = list(dict.fromkeys(country))
    country = ', '.join(map(str, country))

    deleter()

    f = open(filename, "w")
    f.write(str(counter))
    f.close()
    
    f= open(countryfile, "a")
    f.write("\n")
    f.write(ipcountry)
    f.close()
  
    up()


app = Flask(__name__)


@app.route("/")
def index():
    global yourip
    # take the visitor ip
    yourip = request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr)
    
    geo()
  
    main()


    random_number = random.randint(1, 1000)
    return render_template(
        "index.html",
        random_number=random_number,
        counter=counter,
        yourip=yourip,
        ipcountry=ipcountry,
        country=country,
        maxcountry=maxcountry
    )
