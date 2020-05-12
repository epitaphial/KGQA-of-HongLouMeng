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
    data = graph.run(
    "match(p)-[r]->(n:Person{Name:'%s'}) return  p.Name,r.relation,n.Name,p.cate,n.cate\
        Union all\
    match(p:Person {Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.cate, n.cate" % (name,name)
    )
    data = list(data)
    return data