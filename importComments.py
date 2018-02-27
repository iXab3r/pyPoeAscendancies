import praw
from praw.models import MoreComments
from poeShared import *
from pathlib import Path
import jsonpickle

settings = {
    'user-agent':'User-Agent: poeAscendancyRevamp:v0.0.1 (by /u/xab3r)',
    'clientId':'',
    'clientSecret':'',
    'clientUsername':'',
    'clientPassword':'',
}

settingsFile = Path(".settings")
if not settingsFile.is_file():
    with open('.settings', 'w') as settingsFile:
        settingsFile.write(jsonpickle.encode(settings, unpicklable=True))
    raise Exception("Please fill out settings file first")
else:
    settings = jsonpickle.decode(settingsFile.read_text())

pprint(settings)

r = praw.Reddit(client_id=settings['clientId'],
                client_secret=settings['clientSecret'],
                password=settings['clientPassword'],
                user_agent=settings['user-agent'],
                username=settings['clientUsername'])

print('Authenticated as {}'.format(r.user.me()))

def get_comments(submission, n=0):
    print('Requesting {} comments from {}'.format(n if n > 0 else 'all', submission))
    count = 0

    def barf_comments(iterable=submission.comments):
        nonlocal count
        for c in iterable:
            if isinstance(c, MoreComments):
                yield from barf_comments(c.comments())
                continue

            if hasattr(c, 'body') and (n == 0 or count < n):
                count += 1
                yield c

            if c.replies is not None:
                yield from barf_comments(c.replies)

    return barf_comments()


print('Recreating database...')
dbRecreate()

subredditsToAnalyze=[
    # Duelist
    SubredditInfo(ascendancy=PoeAscendancy.Gladiator, url='https://www.reddit.com/r/pathofexile/comments/80g6no/revamped_ascendancy_class_reveal_gladiator/'),
    SubredditInfo(ascendancy=PoeAscendancy.Gladiator, url='https://www.reddit.com/r/pathofexile/comments/80ggz9/a_quick_comparison_overview_for_the_gladiator/'),
    SubredditInfo(ascendancy=PoeAscendancy.Champion, url='https://www.reddit.com/r/pathofexile/comments/7z9oew/check_out_the_new_champion_ascendancy/'),
    SubredditInfo(ascendancy=PoeAscendancy.Champion, url='https://www.reddit.com/r/pathofexile/comments/7z9vz4/32_champion_ascendancy/'),
    SubredditInfo(ascendancy=PoeAscendancy.Slayer, url='https://www.reddit.com/r/pathofexile/comments/808nzk/revamped_ascendancy_class_reveal_slayer/'),
    SubredditInfo(ascendancy=PoeAscendancy.Slayer, url='https://www.reddit.com/r/pathofexile/comments/808yxc/and_here_is_the_overview_of_the_slayer_changes_in/'),

    # Templar
    SubredditInfo(ascendancy=PoeAscendancy.Inquisitor, url='https://www.reddit.com/r/pathofexile/comments/80i2ru/revamped_ascendancy_class_reveal_inquisitor/'),
    SubredditInfo(ascendancy=PoeAscendancy.Guardian, url='https://www.reddit.com/r/pathofexile/comments/7z1ssy/image_assassin_hierophant_guardian_changes/'),
    SubredditInfo(ascendancy=PoeAscendancy.Guardian, url='https://www.reddit.com/r/pathofexile/comments/7z23sy/32_assassin_guardian_and_hierophant_ascendancies/'),
    SubredditInfo(ascendancy=PoeAscendancy.Hierophant, url='https://www.reddit.com/r/pathofexile/comments/7z1ssy/image_assassin_hierophant_guardian_changes/'),
    SubredditInfo(ascendancy=PoeAscendancy.Hierophant, url='https://www.reddit.com/r/pathofexile/comments/7z23sy/32_assassin_guardian_and_hierophant_ascendancies/'),

    # Witch
    SubredditInfo(ascendancy=PoeAscendancy.Necromancer, url='https://www.reddit.com/r/pathofexile/comments/80flcr/revamped_ascendancy_class_reveal_necromancer/'),
    SubredditInfo(ascendancy=PoeAscendancy.Necromancer, url='https://www.reddit.com/r/pathofexile/comments/80fz1q/here_it_is_again_a_quick_overview_of_the_changes/'),
    SubredditInfo(ascendancy=PoeAscendancy.Elementalist, url='https://www.reddit.com/r/pathofexile/comments/8083i1/ive_made_a_quick_overview_of_the/'),
    SubredditInfo(ascendancy=PoeAscendancy.Elementalist, url='https://www.reddit.com/r/pathofexile/comments/807t7s/revamped_ascendancy_class_reveal_elementalist/'),
    SubredditInfo(ascendancy=PoeAscendancy.Occultist, url='https://www.reddit.com/r/pathofexile/comments/80920p/revamped_ascendancy_class_reveal_occultist/'),
    SubredditInfo(ascendancy=PoeAscendancy.Occultist, url='https://www.reddit.com/r/pathofexile/comments/8098w9/a_quick_overview_of_the_changes_for_the_revamped/'),

    #Ranger
    SubredditInfo(ascendancy=PoeAscendancy.Deadeye, url='https://www.reddit.com/r/pathofexile/comments/808ai8/revamped_ascendancy_class_reveal_deadeye/'),
    SubredditInfo(ascendancy=PoeAscendancy.Deadeye, url='https://www.reddit.com/r/pathofexile/comments/808hzc/here_you_go_a_quick_overview_of_the_revamped/'),
    SubredditInfo(ascendancy=PoeAscendancy.Raider, url='https://www.reddit.com/r/pathofexile/comments/7zi9nh/heres_todays_ascendancy_class_update_the_raider/'),
    SubredditInfo(ascendancy=PoeAscendancy.Raider, url='https://www.reddit.com/r/pathofexile/comments/7zieef/32_raider_ascendancy/'),
    SubredditInfo(ascendancy=PoeAscendancy.Pathfinder, url='https://www.reddit.com/r/pathofexile/comments/7z95ju/image_32_pathfinder/'),
    SubredditInfo(ascendancy=PoeAscendancy.Pathfinder, url='https://www.reddit.com/r/pathofexile/comments/7z9008/as_you_have_seen_most_ascendancy_classes_have/'),

    # Shadow
    SubredditInfo(ascendancy=PoeAscendancy.Trickster, url='https://www.reddit.com/r/pathofexile/comments/809q59/revamped_ascendancy_class_reveal_trickster/'),
    SubredditInfo(ascendancy=PoeAscendancy.Trickster, url='https://www.reddit.com/r/pathofexile/comments/80a003/here_is_the_last_quick_overview_for_today_the/'),
    SubredditInfo(ascendancy=PoeAscendancy.Saboteur, url='https://www.reddit.com/r/pathofexile/comments/80i0ow/a_quick_overview_of_the_changes_made_to_the/'),
    SubredditInfo(ascendancy=PoeAscendancy.Saboteur, url='https://www.reddit.com/r/pathofexile/comments/80i0ow/a_quick_overview_of_the_changes_made_to_the/'),
    SubredditInfo(ascendancy=PoeAscendancy.Assassin, url='https://www.reddit.com/r/pathofexile/comments/7z1ssy/image_assassin_hierophant_guardian_changes/'),
    SubredditInfo(ascendancy=PoeAscendancy.Assassin, url='https://www.reddit.com/r/pathofexile/comments/7z23sy/32_assassin_guardian_and_hierophant_ascendancies/'),

    # Marauder
    SubredditInfo(ascendancy=PoeAscendancy.Berserker, url='https://www.reddit.com/r/pathofexile/comments/807df2/the_beserker_and_chieftain_have_changed_slightly/'),
    SubredditInfo(ascendancy=PoeAscendancy.Chieftain, url='https://www.reddit.com/r/pathofexile/comments/807df2/the_beserker_and_chieftain_have_changed_slightly/'),
]

for subredditInfo in subredditsToAnalyze:
    print('Fetching {}'.format(subredditInfo))
    submission = r.submission(
        url=subredditInfo.url)
    comments = list(get_comments(submission))
    print('Got {} comment(s), pushing into db...'.format(len(comments)))
    for comment in comments:
        dbUpdateComment(subredditInfo, comment)
    dbCommit()
