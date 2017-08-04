from flask import (Flask, redirect, url_for, render_template, 
    request, make_response)
from tinydb import TinyDB, Query
import argparse
import os
import uuid
import random

app = Flask(__name__)


# Carga base de datos de conversaciones
db = TinyDB('conversations.json')
Usuario= Query()

queries={}
for root, dirs, files in os.walk("data"):
    for name in files:
        ALGS=[]
        for line in open(os.path.join(root, name)):
            line=line.strip()
            if line.startswith('ALGORITMO'):
                alg=line
                ALGS.append([])
            else:
                bits=line.split()
                ALGS[-1].append(tuple(bits))
        queries[name]=ALGS
         

@app.route('/rj/')
def login():
  return render_template('home.html')

@app.route('/rj/eval')
def eval():
    user_id = request.cookies.get('user_id')
    user=db.search(Usuario.user_id == user_id)
    if user_id and len(user)>0:
        if user[0].finished:
            return redirect(url_for('.already_answered'))
        else:
            return render_template('eval.html',
                user_id=user_id,
                queries=queries[user.query_id][user[0].page],
                page=user[0].page)
    if len(user)==0 and not user_id:
        user_id=str(uuid.uuid4())
        query_id=random.choice(list(queries.keys()))
        resp = make_response(render_template('eval.html',
                        user_id=user_id,
                        queries=queries[query_id][0],
                        page=0))
        resp.set_cookie('user_id',user_id)
        return resp
    if len(user)==0 and user_id:
        query_id=random.choice(list(queries.keys()))
        return render_template('eval.html',
                user_id=user_id,
                queries=queries[query_id][0],
                page=0)

@app.route('/rj/clear')
def clear():
    resp = make_response(redirect(url_for('.eval')))
    resp.set_cookie('user_id',expires=0)
    return resp

@app.route('/rj/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/rj/question')
def already_answered():
    return render_template('thanks.html')

@app.route('/rj/new_user')
def new_user():
    user_id=str(uuid.uuid4())
    resp = make_response(render_template('eval.html',user_id=user_id,page=0))
    resp.set_cookie('user_id',user_id)
    return resp


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
