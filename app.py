from neo_db.query_graph import query_all,query_name,query_by_sentence
from hlp.hlp import Hlp
from flask import Flask,jsonify,render_template,request,escape

app = Flask(__name__)

@app.route('/')
def hlm_index():
    return render_template('index.html')

@app.route('/getallrela')
def get_all_relation():
    nodes,edges = query_all()
    nodesList = list(nodes)
    nodeslist2 = list()
    for li in nodesList:
        if li not in nodeslist2 and li != None:
            nodeslist2.append(li)
    return jsonify({"nodes": nodesList, "edges": list(edges)})

@app.route('/allrelation')
def show_all_relation():
    return render_template('allrelation.html')

@app.route('/searchedrela',methods=['GET', 'POST'])
def show_searched_rela():
    if request.method == 'POST':
        name = request.form.get("name")
        return render_template('showsearch.html',thename=name)
    else:
        return render_template('searchbyname.html')

@app.route('/getrela/<name>')
def get_rela_by_name(name):
    nodes,edges = query_name(name)
    nodesList = list(nodes)
    nodeslist2 = list()
    for li in nodesList:
        if li not in nodeslist2 and li != None:
            nodeslist2.append(li)
    nodeslist3 = list()
    emptylist = []
    for i in nodeslist2:
        if (type(i) == type(emptylist)):
            if i[0] not in nodeslist3:
                nodeslist3.append(i[0])
            if i[1] not in nodeslist3:
                nodeslist3.append(i[1])
    return jsonify({"nodes": nodeslist3, "edges": list(edges)})

@app.route('/qa',methods=['GET', 'POST'])
def show_searched_sent():
    if request.method == 'POST':
        sentence = request.form.get("sentence")
        return render_template('showqa.html',sent=sentence)
    else:
        return render_template('questionanswer.html')

@app.route('/qa/<sentence>')
def get_rela_by_sentence(sentence):
    nlp = Hlp("../ltp_data_v3.4.0","./raw_data") #ltp模块的路径
    sent_list = nlp.process_ques(sentence); #nh nh r n
    nodes,edges = query_by_sentence(sent_list)
    emptylist = []
    if(type(nodes) == type(emptylist)):
        nodeslist3 = list()
        for li in nodes:
            if li not in nodeslist3 and li != None:
                nodeslist3.append(li)
    else:
        nodesList = list(nodes)
        nodeslist2 = list()
        for li in nodesList:
            if li not in nodeslist2 and li != None:
                nodeslist2.append(li)
        nodeslist3 = list()
        for i in nodeslist2:
            if (type(i) == type(emptylist)):
                if i[0] not in nodeslist3:
                    nodeslist3.append(i[0])
                if i[1] not in nodeslist3:
                    nodeslist3.append(i[1])

    if (type(edges) == type(emptylist)):
        edgeslist2 = list()
        for li in edges:
            if li not in edgeslist2 and li != None:
                edgeslist2.append(li)
    else:
        edgesList = list(edges)
        edgeslist2 = list()
        for li in edgesList:
            if li not in edgeslist2 and li != None:
                edgeslist2.append(li)
    #print(nodeslist3)
    return jsonify({"nodes": nodeslist3, "edges": edgeslist2})