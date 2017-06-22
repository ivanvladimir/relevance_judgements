from flask import Flask, redirect, url_for, render_template
import argparse
import os

app = Flask(__name__)


@app.route('/')
def login():
  return render_template('home.html')

@app.route('/eval')
def eval():
  return render_template('home.html')

@app.route('/instructions')
def instructions():
  return render_template('instructions.html')



if __name__ == '__main__':
    p = argparse.ArgumentParser("Twitter ML")
    p.add_argument("--host",default="127.0.0.1",
            action="store", dest="host",
            help="Root url [127.0.0.1]")
    p.add_argument("--port",default=5000,type=int,
            action="store", dest="port",
            help="Port url [500]")
    p.add_argument("--debug",default=False,
            action="store_true", dest="debug",
            help="Use debug deployment [Flase]")
    p.add_argument("-v", "--verbose",
            action="store_true", dest="verbose",
            help="Verbose mode [Off]")

    opts = p.parse_args()

    app.run(debug=opts.debug,
            host=opts.host,
            port=opts.port)
