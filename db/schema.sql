PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sectors(

sector_id INTEGER PRIMARY KEY,

sector_name TEXT UNIQUE NOT NULL

);

CREATE TABLE IF NOT EXISTS companies(

company_id INTEGER PRIMARY KEY,

company_name TEXT NOT NULL,

ticker TEXT UNIQUE,

sector_id INTEGER,

website TEXT,

FOREIGN KEY(sector_id)

REFERENCES sectors(sector_id)

);