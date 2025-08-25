import requests
import sqlite3
import json
import os
from datetime import datetime

LEAGUE_ID=os.getenv("BIWENGER_LEAGUE_ID")

URL_login = 'https://biwenger.as.com/api/v2/auth/login'
URL_account = 'https://biwenger.as.com/api/v2/account'
URL_players_market = 'https://biwenger.as.com/api/v2/user?fields=players(id,owner),market(*,-userID),-trophies'
URL_players_league = 'https://biwenger.as.com/api/v2/players/la-liga/' # ENDPOINT DISABLED
URL_retire_market = "https://biwenger.as.com/api/v2/market?player="
URL_ADD_PLAYER_MARKET = "https://biwenger.as.com/api/v2/market"
URL_ALL_PLAYERS = "https://biwenger.as.com/api/v2/competitions/la-liga/data?lang=es&score=5" #!Dumped
URL_ranking = "https://biwenger.as.com/api/v2/rounds/league"
URL_transfers = f"https://biwenger.as.com/api/v2/league/{LEAGUE_ID}/board?type=transfer,market"

DB_PATH = "la_liga.sqlite"
HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json, text/plain, */*'}

def fetch_general_data() -> dict:
    response = requests.get(URL_ALL_PLAYERS,headers=HEADERS)
    response.raise_for_status()
    return response.json()["data"]

def init_db(conn) -> None:
    '''
    Creates the database structure if it doesn't exist already.
    There's a file:
    - structure.sql - Is based in sqlite database format.
    '''
    cur = conn.cursor()
    try:
        with open("db/structure.sql", "r") as f:
            sql_commands = f.read()
        for command in sql_commands.split(';'):
            if command.strip():
                cur.execute(command)
        conn.commit()
    except Exception as e:
        print(f"Error creating the database structure: {e}")


def update_db(data, conn):
    import pytz
    cur = conn.cursor()

    # Update league
    league = data
    cur.execute("REPLACE INTO league (id, name, slug, sport, currency) VALUES (?, ?, ?, ?, ?)", (
        league["id"], league["name"], league["slug"], league["sport"], league["currency"]
    ))
    cur.execute("INSERT INTO metadata (last_updated, updated_table) VALUES (?, ?)", 
                (datetime.now(pytz.utc).isoformat(), 'league'))

    # Score sources
    for score in league.get("scores", []):
        cur.execute("REPLACE INTO score_sources (id, name, kind) VALUES (?, ?, ?)",
                    (score["id"], score["name"], score["kind"]))               

    # Season
    season = league["season"]
    cur.execute("REPLACE INTO season (id, name, slug, league_id) VALUES (?, ?, ?, ?)",
                (season["id"], season["name"], season["slug"], league["id"]))

    # Rounds
    for rnd in season.get("rounds", []):
        cur.execute("REPLACE INTO round (id, name, short, phase, status, season_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (rnd["id"], rnd["name"], rnd["short"], rnd.get("phase"), rnd["status"], season["id"]))

    cur.execute("INSERT INTO metadata (last_updated, updated_table) VALUES (?, ?)", 
                    (datetime.now(pytz.utc).isoformat(), 'round'))                

    # Active Events
    # * Currently no schema; implement if needed 

    # Teams
    for tid, t in league.get("teams", {}).items():
        cur.execute("REPLACE INTO team (id, name) VALUES (?, ?)", 
                    (t["id"], t["name"]))
    cur.execute("INSERT INTO metadata (last_updated, updated_table) VALUES (?, ?)", 
                    (datetime.now(pytz.utc).isoformat(), 'team'))

    # Players
    for pid, p in league.get("players", {}).items():
        cur.execute(
        """REPLACE INTO player (
            id, name, slug, teamID, position, price, fantasyPrice, status,
            priceIncrement, playedHome, playedAway, points, pointsHome,
            pointsAway, pointsLastSeason, iconHero, statusInfo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        , (
            p["id"], p["name"], p["slug"], p["teamID"], p["position"], p["price"], p["fantasyPrice"], p["status"],
            p["priceIncrement"], p["playedHome"], p["playedAway"], p["points"], p["pointsHome"], p["pointsAway"],
            p.get("pointsLastSeason"), p.get("iconHero"), p.get("statusInfo")
        ))
    cur.execute("INSERT INTO metadata (last_updated, updated_table) VALUES (?, ?)", 
                    (datetime.now(pytz.utc).isoformat(), 'player'))

    conn.commit()

def main():

    data = fetch_general_data()

    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    update_db(data, conn)
    conn.close()

if __name__ == "__main__":
    main()
