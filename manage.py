#!/usr/bin/env python3

# Developer : Hamdy Abou El Anein
# hamdy.aea@protonmail.com


from flask import Flask, render_template, request
import random 
import os
import dropbox

drkey = os.environ["dropkey"]

dbx = dropbox.Dropbox(drkey)

filename = 'visitors.csv'


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
    """
    # if it's the first time. visitors.txt must contain at least 0.
    countfile = "visitors.txt"

    f = open(countfile, "r")
    fileContent = f.read()
    count = int(fileContent) + 1
    f.close()

    f = open(countfile, "w")
    f.write(str(count))
    f.close()

    f = open(countfile,"r")
    counter = f.read()
    f.close()
    """
    random_number = random.randint(1, 1000)
    return render_template('index.html', random_number=random_number, counter=counter, yourip=yourip)
