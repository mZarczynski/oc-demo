from os import environ
from platform import node
from random import random
from flask import Flask,render_template
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def host():
    """Return hostname and environment"""
    return render_template('host.html',name=node(),envs=environ)

@app.route("/cpu/<int:n>/<int:r>")
def cpu(n=1,r=100000):
    """Simulates CPU load by sorting random values. Return hostname and time it took"""
    start = datetime.now()
    for x in range (n):
        l = [random() for i in range(r)]
        l.sort()
    return "Sort took %s on host %s\n"%(datetime.now()-start, node())



if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")