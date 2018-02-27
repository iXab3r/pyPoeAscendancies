from poeShared import *
from textblob.classifiers import NaiveBayesClassifier
import numpy as np
import terminaltables
from terminaltables import AsciiTable

dbRecreate()
print('Number of rows in DB: {}'.format(dbCount()))

rowsPerAscendancy = dict()
for ascendancy in PoeAscendancy:
    rowsPerAscendancy[ascendancy.name] = dbCount(ascendancy)

pprint(rowsPerAscendancy)

resultsByAscendancy = dict()

ascendanciesToProcess = PoeAscendancy#[PoeAscendancy.Elementalist]  # PoeAscendancy# [PoeAscendancy.Pathfinder]

train = [
    ('This is an amazing place!', 'pos'),
    ('I feel very good about these beers.', 'pos'),
    ('blows all the other Ascendancies out of the water', 'pos'),
    ('I want this', 'pos'),
    ('looks great', 'pos'),
    ('woo', 'pos'),
    ('stand out more on her own', 'pos'),
    ('instead of being overshadowed', 'pos'),
    ('Holy fuck, elementalist is now insane', 'pos'),
    ('I was looking forward to this Ascendency the most and it did not disappoint', 'pos'),
    ('GGG now Golemmancer is viable', 'pos'),
    ('Looks awesomely viable', 'pos'),
    ('HYPE!!!', 'pos'),
    ('hype', 'pos'),
    ('is actually looking pretty solid', 'pos'),
    ('pretty solid', 'pos'),
    (' Hey thanks for doing this! Great work', 'pos'),
    ('Your build sounds sick, got a link', 'pos'),
    ('sick', 'pos'),
    ('respectable', 'pos'),
    ('Dark Pact totems Hierophant, because Hiero looks insanely strong.', 'pos'),
    ('looks insanely strong.', 'pos'),
    ('just happy not to be nerfed', 'pos'),
    ('buffed', 'pos'),
    ('Nicer, thanks.', 'pos'),
    ('sounds amazing.', 'pos'),
    ('amazing', 'pos'),
    ('Ah. Oops. Fixed ;)', 'pos'),
    (':)', 'pos'),
    ('Your build sounds sick', 'pos'),
    ('I am very tempted ', 'pos'),
    ('nonironic celebration', 'pos'),
    ("it's fun as hell and will probably be hilarious", 'pos'),
    ("fun as hell", 'pos'),
    ("better now ", 'pos'),
    ("looks cool", 'pos'),
    ("start looks promising", 'pos'),
    ("Got some sick", 'pos'),
    ("positive", 'pos'),

    ("make this ascendancy a joke ", 'neg'),
    ("the worst ascendancy class", 'neg'),
    ("the worst", 'neg'),
    ("Yikes, better luck next", 'neg'),
    ("Was really hoping for this. I guess not", 'neg'),
    (" Feels lazy", 'neg'),
    (" Feels halfassed", 'neg'),
    (" Feels lazy, halfassed, and rushed, bummer", 'neg'),
    (" Feels lazy, halfassed, and rushed, bummer", 'neg'),
    (" bummer", 'neg'),
    (" Feels rushed", 'neg'),
    ("Kind of odd that Hierophant now has 7 major nodes, instead of 6 like every other ascendancy.", 'neg'),
    (":(", 'neg'),
    ("big nerf", 'neg'),
    ("gl hunting beasts in temp league", 'neg'),
    ("nerf", 'neg'),
    ("nerfed", 'neg'),
    ("gonna be bad", 'neg'),
    ("can't easily bleed now", 'neg'),
    ("don't seem to realize", 'neg'),
    ('I do not like', 'neg'),
    ('bonkers', 'neg'),
    ('wasted', 'neg'),
    ('still garbage', 'neg'),
    ('horse shit', 'neg'),
    ('pain in the ass', 'neg'),
    ("I can't deal with this", 'neg'),
    ("My boss is horrible.", "neg"),
    ("huge disappointments", "neg"),
    ("disapointment", "neg"),
    ("it won't happen", "neg"),
    ("screwed", "neg"),
    ("screwed up", "neg"),
    ("as trash as b4", "neg"),
    ("looks shit unfortunately", "neg"),
    ("Timed buffs are shit", "neg"),
    ("I don't see a reason why we can't have", "neg"),
    ("Was there before", "neg"),
    ("Seriously?", "neg"),
    ("kill shaper within a month", "neg"),
]

blobClassifier = NaiveBayesClassifier(train)


def isValidComment(comment):
    return (150 >= len(comment.body) >= 10) and (comment.score >= -2)


for ascendancy in ascendanciesToProcess:
    print('Processing ascendancy {}'.format(ascendancy))
    comments = dbGetComments(ascendancy)
    print('Total: {} comment(s)'.format(len(comments)))

    comments = [comment for comment in comments if isValidComment(comment)]
    print('Analyzing {} comment(s)'.format(len(comments)))

    table_data = [
    ]
    table = AsciiTable(table_data)

    for comment in comments:
        print('processing {}'.format(strFlatten(comment.body)))

        blobClassification = blobClassifier.prob_classify(comment.body)
        comment.polarity = blobClassification.prob("pos")
        if 0.4 <= comment.polarity <= 0.6:
            comment.polarity = 0.5

        table_data.append([comment.polarity, strFlatten(comment.body)])

    table_data.sort(key=lambda tup: tup[0])
    table_data.insert(0, ['Polarity', 'Text'])

    print(table.table)
    avg_polarity = np.mean([comment.polarity for comment in comments]) if len(comments) > 0 else 0

    result = dict([
        ['Polarity', float(avg_polarity)],
    ])
    resultsByAscendancy[ascendancy] = result

pprint(resultsByAscendancy)

print('Updating db...')
dbUpdateStats(resultsByAscendancy)

polarityByAscendancy = dict()
for key in resultsByAscendancy:
    polarity = resultsByAscendancy[key]["Polarity"]
    if polarity <= 0.001:
        continue
    polarityByAscendancy[key.name] = polarity
pprint(polarityByAscendancy)

leastPopular = min(polarityByAscendancy, key=polarityByAscendancy.get)
mostPopular = max(polarityByAscendancy, key=polarityByAscendancy.get)
print('Min: {} Max: {}'.format(leastPopular, mostPopular))
