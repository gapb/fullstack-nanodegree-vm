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

-- I'm not sure if this wholly necessary.
-- matches table prevents rematches by asserting player1 and player2 as
-- primary keys
CREATE TABLE matches (
  player1ID INTEGER,
  player2ID INTEGER,
  winnerID INTEGER,
  PRIMARY KEY (player1ID, player2ID),
  FOREIGN KEY (player1ID) REFERENCES players(id),
  FOREIGN KEY (player2ID) REFERENCES players(id),
  FOREIGN KEY (winnerID) REFERENCES players(id),
  CHECK (player1ID < player2ID)
);

CREATE INDEX playersByWins
ON players(wins, matches, id);

CREATE INDEX matchesByP2
ON matches(player2ID, player1ID);

CREATE INDEX matchesByWinner
ON matches(winnerID, player1ID, player2ID);

