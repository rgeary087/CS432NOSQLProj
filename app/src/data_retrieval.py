from neo4j import GraphDatabase
import time
import pandas
import pprint

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "test"))

def dribblePlayers(tx):
    result = tx.run("MATCH (a:Player) - [i:played_for] -> (x:Season) <- [:played_for] - (b:Player) - [j:played_for] -> (y:Season) <- [k:played_for] - (c:Player) USING JOIN on b WHERE a.id <> b.id AND b.id <> c.id AND a.id <> c.id AND (x.team <> y.team OR (x.season <> y.season AND x.team = y.team)) AND toFloat(i.ws) >= 6.0 AND toFloat(k.ws) >=6.0  RETURN a, b, c, i, j")
    values = [record.values() for record in result]
    return values

def defenderScorer(tx):
    result = tx.run(" MATCH (a:Player) - [i:played_for] -> (x:Season) <- [k:played_for] - (b:Player) WHERE a.id <> b.id AND toFloat(i.ws) >= 5.0 AND toFloat(k.ws) >=5.0 AND (toFloat(i.total_blocks) > 200 OR toFloat(i.total_rebounds) > 800) AND toFloat(k.total_points) > 1750 RETURN DISTINCT a.name as Name1, b.name as Name2,i.total_rebounds as Total_Rebounds,i.total_blocks as Total_Blocks,k.total_points as Total_Points")
    values = [record.values() for record in result]
    return values

def bestTeam(tx):
    result = tx.run("MATCH (t:Team) CALL{  WITH t  MATCH (t) - [to:team_of] - (s:Season)  CALL{      WITH s      MATCH (p:Player) - [pf:played_for] -> (s)      RETURN COLLECT(toInteger(pf.ws)) as playerTop  }  RETURN REDUCE(pl = 0, x IN playerTop | pl + x) AS Total_Win_Shares, MAX(playerTop) as maximum, s as Season } RETURN Season.team as Team, Season.season as Season , Total_Win_Shares, maximum[8..] as Top_2_Players ORDER BY Total_Win_Shares DESC  LIMIT 40")
    values = [record.values() for record in result]
    return values

def parseDefenderOffensiveData():
    ret = session.execute_read(defenderScorer)
    Player1 = [i[0] for i in ret]
    Player2 = [i[1] for i in ret]
    Player1_Rebounds = [i[2] for i in ret]
    Player1_Blocks = [i[3] for i in ret]
    Player2_Points = [i[4] for i in ret]
    parsedData = {'Player 1 |':Player1,
        'Player 2 |':Player2,
        'Player 1 Rebounds |':Player1_Rebounds,
        'Player 1 Blocks |':Player1_Blocks,
        'Player 2 Points |':Player2_Points }
    print(pandas.DataFrame(parsedData))

def parseBestTeamData():
    ret = session.execute_read(bestTeam)
    Team = [i[0] for i in ret]
    Season = [i[1] for i in ret]
    WinShares = [i[2] for i in ret]
    ListOfWinShares = [i[3] for i in ret]
    parsedData = {'Team |':Team,
        'Season |':Season,
        'Win Shares |':WinShares,
        'List of Players by Win Share':ListOfWinShares}
    print(pandas.DataFrame(parsedData))
    #pprint.pprint(ret)

with driver.session() as session:
    timeCurr = time.gmtime()
    #parseDefenderOffensiveData()
    parseBestTeamData()
    #ret = session.execute_read(dribblePlayers)
    #pprint.pprint(ret)
    print(time.gmtime())
    print(timeCurr)
    #[print(a) for a in ret]


driver.close()