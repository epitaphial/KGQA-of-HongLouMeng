from neo_db.config import graph

def buildNodes(nodeRecord):
    if nodeRecord['p.Clan'] == None:
        return
    data = {"name": str(nodeRecord['p.Name']), "clan": str(nodeRecord['p.Clan'])}
    rdata1 = {"data":data}
    if('n.Name' in nodeRecord and 'n.Clan' in nodeRecord):
        if nodeRecord['n.Clan'] == None:
            return
        data2 = {"name": str(nodeRecord['n.Name']), "clan": str(nodeRecord['n.Clan'])}
        rdata2 = {"data":data2}
        return [rdata1,rdata2]
    else:
        return {"data": data}

def buildNodes2(nodeRecord):
    nodedata = []
    for node in nodeRecord['nodes']:
        data = {"name":node['Name'],"clan":node["Clan"]}
        nodedata.append(data)
    return nodedata

def buildEdges(relationRecord):
    data = {"source": str(relationRecord['p.Name']), 
    "target": str(relationRecord['n.Name']),
    "relationship": relationRecord['r.relation']}
    return {"data": data}

def buildEdges2(relationRecord):
    count = 0
    data = []
    for i in relationRecord['shortpath'].relationships:
        data.append({"source": relationRecord['nodes'][count]['Name'], 
        "target": relationRecord['nodes'][count + 1]['Name'],
        "relationship": i['relation']})
        count += 1
    return data

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
    if(sent_list[0]==1):
        #build nodes 焦大和尤氏
        nodes1 = map(buildNodes2, graph.run("match t = allshortestPaths((p:Person) -[*]->(n:Person)) WHERE p.Name = '%s' and n.Name = '%s' return t as shortpath, NODES(t) AS nodes Union all match t = allshortestPaths((p:Person) -[*]->(n:Person)) WHERE p.Name = '%s' and n.Name = '%s' return t as shortpath, NODES(t) AS nodes"% (sent_list[1],sent_list[2],sent_list[2],sent_list[1])).data())        
        nodes = []
        for i in list(nodes1):
            for ii in i:
                tmpdict = {}
                tmpdict['data'] = ii
                nodes.append(tmpdict)
        #build edges
        edges1 = map(buildEdges2, graph.run("match t = allshortestPaths((p:Person) -[*]->(n:Person)) WHERE p.Name = '%s' and n.Name = '%s' return t as shortpath, NODES(t) AS nodes Union all match t = allshortestPaths((p:Person) -[*]->(n:Person)) WHERE p.Name = '%s' and n.Name = '%s' return t as shortpath, NODES(t) AS nodes"% (sent_list[1],sent_list[2],sent_list[2],sent_list[1]) ).data())
        edgelist = list(edges1)
        edges = []
        for i in edgelist:
            for ii in i:
                tmpdict = {}
                tmpdict['data'] = ii
                edges.append(tmpdict)
        return nodes,edges
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