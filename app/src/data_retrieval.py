from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "test"))

def dribblePlayers(tx):
    return tx.run()
with driver.session() as session:

    ret = session.run("MATCH (a:Player) - [i:played_for] -> (x:Season) <- [:played_for] - (b:Player) - [j:played_for] -> (y:Season) <- [k:played_for] - (c:Player) USING JOIN on b WHERE a.id <> b.id AND b.id <> c.id AND a.id <> c.id AND (x.team <> y.team OR (x.season <> y.season AND x.team = y.team)) AND toFloat(i.ws) >= 6.0 AND toFloat(k.ws) >=6.0  RETURN a, b, c, i, j")

print(ret["a"])

driver.close()