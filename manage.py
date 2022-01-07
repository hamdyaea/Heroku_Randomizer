#!/usr/bin/env python3

# Developer : Hamdy Abou El Anein
# hamdy.aea@protonmail.com


from flask import Flask, render_template
import random 


app = Flask(__name__)

@app.route('/')
def index():
    random_number = random.randint(1, 1000)
    return render_template('index.html', random_number=random_number)
