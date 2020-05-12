from neo_db.query_graph import query_all
from flask import Flask,jsonify,render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/getallrela')
def get_all_relation():
    nodes,edges = query_all()
    return jsonify({"nodes": list(nodes), "edges": list(edges)})