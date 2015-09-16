-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  wins INTEGER DEFAULT 0,
  matches INTEGER DEFAULT 0
);

-- Table for storing match results. TODO accommodate ties?
CREATE TABLE matches (
  winnerID INTEGER,
  loserID INTEGER,
  PRIMARY KEY (winnerID, loserID),
  FOREIGN KEY (winnerID) REFERENCES players(id),
  FOREIGN KEY (loserID) REFERENCES players(id)
);

CREATE INDEX playersByWins
ON players(wins, matches, id);

CREATE INDEX matchesByLoser
ON matches(loserID, winnerID);

