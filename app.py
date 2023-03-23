from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS= [
    {'id' : 1,
     'title': 'AI Engineer',
     'location': 'Netherlands, Rotterdam',
     'salaris': 3500
     },
{'id' : 4,
     'title': 'Front-end Developer',
     'location': 'Netherlands, Arnhem',
     'salaris': 2900
     },

{'id' : 1,
     'title': 'Data Analist',
     'location': 'Netherlands, Amsterdam',
     'salaris': 4500
     },
{'id' : 1,
     'title': 'App Developer',
     'location': 'Netherlands, Utrecht',
     'salaris': 3200
     }
]
@app.route("/")
def hello_world():
    return render_template('home.html',
                           jobs=JOBS)
@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)