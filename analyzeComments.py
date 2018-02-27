from poeShared import *
from textblob.classifiers import NaiveBayesClassifier
import numpy as np

dbRecreate()
print('Number of rows in DB: {}'.format(dbCount()))

rowsPerAscendancy = dict()
for ascendancy in PoeAscendancy:
    rowsPerAscendancy[ascendancy.name] = dbCount(ascendancy)

pprint(rowsPerAscendancy)

resultsByAscendancy = dict()

ascendanciesToProcess = PoeAscendancy#[PoeAscendancy.Saboteur]# PoeAscendancy# [PoeAscendancy.Pathfinder]

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

for ascendancy in ascendanciesToProcess:
    print('Processing ascendancy {}'.format(ascendancy))
    rawComments = dbGetComments(ascendancy)
    cmts = [line["body"] for line in rawComments]
    print('Analyzing {} comment(s)'.format(len(cmts)))

    sentiments = []
    for body in cmts:
        if len(body) > 150 or len(body) < 10:
            continue
        print('processing {}'.format(body))

        blobClassification = blobClassifier.prob_classify(body)
        blobClassificationPolarity = blobClassification.prob("pos")
        if blobClassification.prob("pos") < 0.5 and blobClassification.prob("neg") < 0.5:
            # avg
            sentiments.append(0.5)
            continue

        sentiments.append(blobClassification.prob("pos"))
        print('\t result: {}\n'.format(blobClassification.prob("pos")))

    avg_polarity = np.mean(sentiments) if len(sentiments) > 0 else 0

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


