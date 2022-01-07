#!/usr/bin/env python3

# Developer : Hamdy Abou El Anein
# hamdy.aea@protonmail.com


from flask import Flask, render_template, request
import random 

app = Flask(__name__)

@app.route('/')
def index():
    # take the visitor ip
    yourip = request.remote_addr
    
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

    random_number = random.randint(1, 1000)
    return render_template('index.html', random_number=random_number, counter=counter, yourip=yourip)
