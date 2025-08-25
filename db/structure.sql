BEGIN;

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS league (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        slug TEXT,
        sport TEXT,
        currency TEXT
    );

    CREATE TABLE IF NOT EXISTS score_sources (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        kind TEXT
    );

    CREATE TABLE IF NOT EXISTS season (
        id TEXT PRIMARY KEY,
        name TEXT,
        slug TEXT,
        league_id INTEGER,
        FOREIGN KEY (league_id) REFERENCES league(id)
    );

    CREATE TABLE IF NOT EXISTS round (
        id INTEGER PRIMARY KEY,
        name TEXT,
        short TEXT,
        phase INTEGER,
        status TEXT,
        season_id TEXT,
        FOREIGN KEY (season_id) REFERENCES season(id)
    );

    CREATE TABLE IF NOT EXISTS team (
        id INTEGER PRIMARY KEY,
        name TEXT
    );

    CREATE TABLE IF NOT EXISTS player (
        id INTEGER PRIMARY KEY,
        name TEXT,
        slug TEXT,
        teamID INTEGER,
        position INTEGER,
        price INTEGER,
        fantasyPrice INTEGER,
        status TEXT,
        priceIncrement INTEGER,
        playedHome INTEGER,
        playedAway INTEGER,
        points INTEGER,
        pointsHome INTEGER,
        pointsAway INTEGER,
        pointsLastSeason INTEGER,
        iconHero TEXT,
        statusInfo TEXT,
        FOREIGN KEY (teamID) REFERENCES team(id)
    );

    CREATE TABLE IF NOT EXISTS market_data (
        id INTEGER PRIMARY KEY,
        date TEXT,
        until TEXT,
        price INTEGER,
        player_id INTEGER,
        user_id INTEGER,
        name TEXT,
        slug TEXT,
        teamID INTEGER,
        position INTEGER,
        fantasyPrice INTEGER,
        status TEXT,
        priceIncrement INTEGER,
        playedHome INTEGER,
        playedAway INTEGER,
        fitness TEXT,
        points INTEGER,
        pointsHome INTEGER,
        pointsAway INTEGER,
        pointsLastSeason INTEGER
    );

    CREATE TABLE IF NOT EXISTS metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_updated TEXT,
        updated_table TEXT);