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

dbx = dropbox.Dropbox(drkey)

filename = 'visitors.csv'

def geo():
    global ipcountry
    ip = "83.222.156.104"
    backadrr = "https://www.ipinfo.io/"
    fulladd = backadrr+str(ip)

    r = requests.get(fulladd)
    data = r.json()
    ipcountry = data["country"]

def up():
    with open(filename, "rb") as f:
        dbx.files_upload(f.read(),'/'+filename)

def down():
    dbx.files_download_to_file(filename,"/"+filename)

def deleter():
    dbx.files_delete("/"+filename)

def main():
    global counter
    try:
        down()
    except:
        pass

    f = open(filename, "r")
    value = f.read()

    counter = int(value)  + 1

    try:
        deleter()
    except:
        pass

    f = open(filename, "w")
    f.write(str(counter))
    f.close()

    up()

    


app = Flask(__name__)

@app.route('/')
def index():
    # take the visitor ip
    #yourip = request.remote_addr
    yourip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    
    main()
    
    geo()
    
    random_number = random.randint(1, 1000)
    return render_template('index.html', random_number=random_number, counter=counter, yourip=yourip, ipcountry=ipcountry)
