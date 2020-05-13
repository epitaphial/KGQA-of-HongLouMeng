from neo_db.config import graph

def buildNodes(nodeRecord):
    if nodeRecord['p.Clan'] == None:
        return
    else:
        data = {"name": str(nodeRecord['p.Name']), "clan": str(nodeRecord['p.Clan'])}
        return {"data": data}


def buildEdges(relationRecord):
    data = {"source": str(relationRecord['p.Name']), 
    "target": str(relationRecord['n.Name']),
    "relationship": relationRecord['r.relation']}
    return {"data": data}

def query_all():
    nodes = map(buildNodes, graph.run('MATCH (p) RETURN p.Name, p.Clan').data())
    edges = map(buildEdges, graph.run('MATCH (p)-[r]->(n) RETURN p.Name, r.relation,n.Name').data())
    return nodes,edges

def query_name(name):
    nodes = map(buildNodes, graph.run("match(p)-[r]->(n:Person{Name:'%s'}) return p.Name,n.Name,p.Clan,n.Clan\
        Union all\
    match(p:Person {Name:'%s'}) -[r]->(n) return p.Name,n.Name,p.Clan,n.Clan" % (name,name)).data())

    edges = map(buildEdges, graph.run("match(p)-[r]->(n:Person{Name:'%s'}) return p.Name, r.relation,n.Name\
        Union all\
    match(p:Person {Name:'%s'}) -[r]->(n) return p.Name, r.relation,n.Name" % (name,name)).data())
    return nodes,edges

def query_by_sentence(sent_list):
    print(sent_list)
    if(sent_list[0]==1):
        nodes = map(buildNodes, graph.run("match(p:Person {Name:'%s'}) -[r]->(n:Person {Name:'%s'}) return p.Name,n.Name,p.Clan,n.Clan\
        Union all\
    match(p:Person {Name:'%s'}) -[r]->(n:Person {Name:'%s'}) return p.Name,n.Name,p.Clan,n.Clan" % (sent_list[1],sent_list[2],sent_list[2],sent_list[1])).data())
        edges = map(buildEdges, graph.run("match(p:Person {Name:'%s'}) -[r]->(n:Person {Name:'%s'}) return p.Name, r.relation,n.Name\
        Union all\
    match(p:Person {Name:'%s'}) -[r]->(n:Person {Name:'%s'}) return p.Name, r.relation,n.Name" % (sent_list[1],sent_list[2],sent_list[2],sent_list[1])).data())
    elif(sent_list[0]==2):
        nodes = map(buildNodes, graph.run("match(n:Person{Name:'%s'})-[r:%s{relation: '%s'}]->(p) return p.Name,n.Name,p.Clan,n.Clan \
        Union all\
            match(p:Person{Name:'%s'})-[r:%s{relation: '%s'}]->(n) \
         return p.Name,n.Name,p.Clan,n.Clan" % (sent_list[1],sent_list[3],sent_list[3],sent_list[1],sent_list[3],sent_list[3])).data())
        edges = map(buildEdges, graph.run("match(p:Person{Name:'%s'})-[r:%s{relation: '%s'}]->(n) return p.Name, r.relation,n.Name" % (sent_list[1],sent_list[3],sent_list[3])).data())
    elif(sent_list[0]==3):
        nodes = map(buildNodes, graph.run("match(n)-[r:%s{relation: '%s'}]->(p:Person{Name:'%s'}) return p.Name,n.Name,p.Clan,n.Clan \
        Union all\
            match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) \
         return p.Name,n.Name,p.Clan,n.Clan" % (sent_list[3],sent_list[3],sent_list[2],sent_list[3],sent_list[3],sent_list[2])).data())
        edges = map(buildEdges, graph.run("match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) return p.Name, r.relation,n.Name" % (sent_list[3],sent_list[3],sent_list[2])).data())
    else:
        pass
    return nodes,edges