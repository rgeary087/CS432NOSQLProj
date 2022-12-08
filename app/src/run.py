import pandas as pd
from neo4j import GraphDatabase

teams = [
    "76ers",
    "bucks",
    "bulls",
    "cavs",
    "celtics",
    "clippers",
    "grizzlies",
    "hawks",
    "heat",
    "hornets",
    "jazz",
    "kings",
    "knicks",
    "lakers",
    "magic",
    "mavericks",
    "nets",
    "nuggets",
    "pacers",
    "pelicans",
    "pistons",
    "raptors",
    "rockets",
    "spurs",
    "suns",
    "thunder",
    "timberwolves",
    "trailblazers",
    "warriors",
    "wizards",
]

teamCSVList = []

columnNames = [
    "Row",
    "Player",
    "WS",
    "WS+",
    "Season",
    "Age",
    "Team",
    "G",
    "GS",
    "MP",
    "FG",
    "FGA",
    "2P",
    "2PA",
    "3P",
    "3PA",
    "FT",
    "FTA",
    "ORB",
    "DRB",
    "TRB",
    "AST",
    "STL",
    "BLK",
    "TOV",
    "PF",
    "PTS",
    "FG%",
    "2P%",
    "3P%",
    "FT%",
    "TS%",
    "eFG%",
    "Pos",
    "PID"
]

for i in teams:
    teamCSV = pd.read_csv(f"data/{i}.csv", names = ["column"])
    teamCSV[columnNames] = teamCSV["column"].apply(lambda x: pd.Series(str(x)[1:-1].split(",")))
    teamCSVList.append(teamCSV)

print("DATA READ DONE")
print("Connecting to NEO4J")

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "test"))

def db_clear(tx):
    tx.run("MATCH (a) -[r] -> () DELETE a, r")
    tx.run("MATCH (a) DELETE a")

def create_team(tx, team):
    tx.run("CREATE (a:Team {name: $team})", team=team)
    

def create_player(tx, player, team):
    tx.run("MERGE (season:Season {team: $team, season: $season})"
           "MERGE (player:Player {id: $id, name: $name})"
           "MERGE (team:Team {name: $team})"
           "MERGE (season)-[:team_of {dummy: '123'}]->(team)"
           "MERGE (player)-[:played_for {ws: $win_share, ppg: $ppg}]->(season)",
           id=player.loc["PID"], team=team, season=player.loc["Season"], win_share = player.loc["WS"], name = player.loc["Player"], ppg = player.loc["PTS"])
    

with driver.session() as session:
    #DB Reset
    session.execute_write(db_clear)
    
    #Creating Teams
    for i in teams:
        session.execute_write(create_team, i)
        print(f"Created {i}")
    for i in range(0, len(teamCSVList)):
        teamCSVList[i][teamCSVList[i]["Season"] >= "2000"].apply(axis = 1, func =lambda x: session.execute_write(create_player, x, teams[i]))
        print(f"Created team {teams[i]}")
    #Populating Players
    # session.execute_write(create_friend_of, "Alice", "Bob")
    # print(f"Created {"Bob"}")
    # session.execute_write(create_friend_of, "Alice", "Carl")
    # print({})

driver.close()

print("NEO4J DONE")