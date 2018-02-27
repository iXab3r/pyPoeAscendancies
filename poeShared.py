import sqlite3
import atexit
from pprint import pprint
from enum import Enum, unique
from namedlist import namedlist

import jsonpickle

Comment = namedlist('Comment', ['body', 'score', 'author', ('polarity', 0), ('weightedScore', 0)])

dbConn = sqlite3.connect('comments.db')
dbConn.row_factory = sqlite3.Row
dbCursor = dbConn.cursor()

class SubredditInfo:
    def __init__(self, **entries): self.__dict__.update(entries)
    def __str__(self):
        return self.__dict__.__str__()

@unique
class PoeAscendancy(Enum):
    Slayer = 1,
    Gladiator = 2,
    Champion = 3,
    Assassin = 4,
    Saboteur = 5,
    Trickster = 6,
    Juggernaut = 7,
    Berserker = 8,
    Chieftain = 9,
    Necromancer = 10,
    Elementalist = 11,
    Occultist = 12,
    Deadeye = 13,
    Raider = 14,
    Pathfinder = 15,
    Inquisitor = 16,
    Hierophant = 17,
    Guardian = 18,
    Ascendant = 19,


ascChanges = dict(
    [[PoeAscendancy.Slayer, ''],
    [PoeAscendancy.Gladiator, ''],
    [PoeAscendancy.Champion, ''],
    [PoeAscendancy.Assassin, ''],
    [PoeAscendancy.Saboteur, ''],
    [PoeAscendancy.Trickster, ''],
    [PoeAscendancy.Juggernaut, ''],
    [PoeAscendancy.Berserker, ''],
    [PoeAscendancy.Chieftain, ''],
    [PoeAscendancy.Necromancer, ''],
    [PoeAscendancy.Elementalist, ''],
    [PoeAscendancy.Occultist, ''],
    [PoeAscendancy.Deadeye, ''],
    [PoeAscendancy.Raider, ''],
    [PoeAscendancy.Pathfinder, ''],
    [PoeAscendancy.Inquisitor, ''],
    [PoeAscendancy.Hierophant, ''],
    [PoeAscendancy.Guardian, ''],
    [PoeAscendancy.Ascendant, '']]
)

def strFlatten(value):
    return "\t".join( value.splitlines())

def dbRecreate():
    #dbCursor.execute('DROP TABLE IF EXISTS comment')
    dbCursor.execute('CREATE TABLE IF NOT EXISTS `comment` (\
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,\
        `r_id`	TEXT,\
        `timestamp`	INTEGER,\
        `score`	INTEGER,\
        `author`	TEXT,\
        `ascendancy`	TEXT,\
        `body`	TEXT\
    )')

    dbCursor.execute('CREATE TABLE IF NOT EXISTS `stats` (\
            `ascendancy`	TEXT NOT NULL PRIMARY KEY UNIQUE,\
            `json`	TEXT\
        )')

    dbCursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS `AscComment` ON `comment` (`r_id`, `ascendancy`)')

def dbUpdateComment(subredditInfo, comment):
    try:
        if (comment.author is None):
            return

        dbCursor.execute('insert or replace into comment (r_id, timestamp, score, author, ascendancy, body) values (?, ?, ?, ?, ?, ?)',
                         (comment.id, comment.created_utc, comment.score, comment.author.name, subredditInfo.ascendancy.name, comment.body))
    except Exception as ex:
        print('Failed to process comment {}'.format(comment))
        pprint(vars(comment))
        raise ex
    return

def dbCommit():
    dbConn.commit()

def dbCount(ascendancy = None):
    query = "SELECT COUNT(*) from `comment`"
    if ascendancy is not None:
        query = query + ' WHERE ascendancy = "{}"'.format(ascendancy.name)
    dbCursor.execute(query)
    return dbCursor.fetchone()[0]

def dbGetComments(ascendancy = None):
    query = "SELECT * from `comment`"
    if ascendancy is not None:
        query = query + ' WHERE ascendancy = "{}"'.format(ascendancy.name)
    dbCursor.execute(query)
    return [Comment(
        body=line['body'],
        score=line['score'],
        author=line['author']) for line in dbCursor.fetchall()]

def dbUpdateStats(statsByAscendancy):
    for key in statsByAscendancy:
        encoded = jsonpickle.encode(statsByAscendancy[key], unpicklable=False)
        dbCursor.execute('insert or replace into stats (ascendancy, json) values (?, ?)',
                     (key.name, encoded))

def dbGetStats(ascendancy = None):
    query = "SELECT * from `stats`"
    if ascendancy is not None:
        query = query + ' WHERE ascendancy = "{}"'.format(ascendancy.name)
    dbCursor.execute(query)
    return dbCursor.fetchall()

@atexit.register
def onExit():
    print("Script is terminating, commiting db changes...")
    dbCursor.close()
    dbConn.commit()
    dbConn.close()