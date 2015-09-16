#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from random import choice


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    curs = db.cursor()
    curs.execute("DELETE FROM matches")
    # Should this similarly reset the players win/loss counts?
    db.commit()
    curs.close()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    # delete from matches, just in case that hasn't been done
    deleteMatches()
    db = connect()
    curs = db.cursor()
    curs.execute("DELETE FROM players")
    db.commit()
    curs.close()
    db.close()



def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    curs = db.cursor()
    curs.execute("SELECT COUNT(*) FROM players")
    result = curs.fetchone()

    count = 0 if result is None else result[0]

    # curs.execute("SELECT id FROM players")
    # # todo: see if I can run len() on curs()
    # # todo: alternately, do this with a query using count(*)
    # count = 0
    # for playerID in curs.fetchall():
    #     ++count
    # curs.close()
    # db.close()
    return count
    # todo: add error handling


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    curs = db.cursor()
    curs.execute("INSERT INTO players (id) VALUES (%s)", (name,))
    db.commit()
    curs.close()
    db.close()
    # todo add error handling


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    curs = db.cursor()
    curs.execute("SELECT * FROM players ORDER BY wins DESC")
    standings = curs.fetchall()
    curs.close()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # TODO add error handling
    # TODO accommodate ties?
    db = connect()
    curs = db.curs()
    # update matches table
    curs.execute("INSERT INTO matches (winnerID, loserID) VALUES (%s, %s)",
                 (winner, loser))
    # update matches count
    curs.execute("UPDATE players SET matches = matches + 1 WHERE id = %s OR "
                 "id = %s", (winner, loser))
    # update winner
    curs.execute("UPDATE players SET wins = wins + 1 WHERE id = %s", (winner,))
    db.commit()
    curs.close()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    curs = db.cursor()
    # Step 1: grab all players.
    # Tuple Order: (ID, name, Wins, Matches, name)
    curs.execute("SELECT id, name, wins, matches FROM players ORDER BY wins, "
                 "matches DESC")

    # First, let's check for the case where no matches have been played yet.
    # We can identify this case by fetching the first tuple, and checking if
    # wins == matches == 0
    players = []
    first_player = curs.fetchone()
    # None check because why not
    if first_player is None:
        return None
    if first_player[2] == 0 and first_player[3] == 0:
        players.append(first_player)
        # also insert everything else into the players list.
        players.extend(curs)
        # create list for pairings
        pairings = []
        # randomly generate pairings, assuming len(players) is even
        while len(pairings) != 0:
            player1 = choice(players)
            players.remove(player1)
            player2 = choice(players)
            players.remove(player2)
            # todo make more efficient?
            pairings.append((player1, player2))
        return pairings
    # Now, if matches have been played, players will need to be a list of lists
    else:
        player_group_id = 0
        players.append([first_player])
        next_player = curs.fetchone()
        while next_player is not None:
            # if numWins is different, we've begun a new group
            if next_player[2] != players[player_group_id][2]:
                players.append([next_player])
                ++player_group_id
            else:
                players[player_group_id].append(next_player)
            next_player = curs.fetchone()
        # Now, having gotten players grouped by numWins, it's time to generate
        # pairings.
        player_group_id = 0
        pairings = []
        while player_group_id < len(players):
            player_group = players[player_group_id]
            # choose player1
            player1 = choice(player_group)
            player_group.remove(player1)
            # choose player2. Assumes subgroups are even—not safe
            if len(player_group) == 0:
                player_group = players[++player_group_id]
            player2 = choice(player_group)
            player_group.remove(player2)
            if len(player_group) == 0:
                ++player_group_id
            pairings.append((player1, player2))
            # TODO check for duplicates
        return pairings








