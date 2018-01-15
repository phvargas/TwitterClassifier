import sys
import os
import re
from textblob import TextBlob
from time import strftime, localtime, time

"""
    Given a file containing the tweets extracted from a conversation and a set of harasser accounts
    gets the terms used by the harassers accounts.    
"""

__author__ = 'Plinio H. Vargas'
__date__ = 'Mon,  Dec 13, 2017 at 10:51'
__email__ = 'pvargas@cs.odu.edu'


def get_tweets(in_file):
    """
    :param in_file: path of harasser tweets file
    :return: void
    """

    harassers = {'JimiBagODonuts', 'Markfortruth24', 'DarleneBrehm', 'sarahsassywilde', 'REALSUPERMAN100',
                'JaguarTraitors', 'Unkindtaternuts', 'ArlNancy', 'BMou82', 'Afrofuturism', 'wnorris90808',
                'greyhound001', 'masonicbee', 'JasonHi40921799', 'cobaltskky', 'ReversingASD', 'gotgt',
                'Charles43553135', 'JulianJ03', 'GrnEyeBuzzard', 'RokedvMagen', 'feminist_truth', 'MO_JO_RZN',
                'cjohnso88', 'LibertyPeak', 'ClintonLost2016', 'SugarsSecrets', 'ddd_deborah', 'KingofCaliforni',
                'docmurdock', 'ImposterBuster', 'isan_og', 'TDR0782', 'ktd101551', 'Badazzmeow', 'RBRadio41',
                'MalisaFSmith', 'DavidCamercon', 'G_Belfort08', 'AllMyGoogles', 'trumptyswall', 'Quotron_Inc',
                'speach_freedom', 'argen_j', 'veganpool', 'Michman75', 'MrTonemonster', 'BobCarr57', 'RashaWasha',
                'lucifersmile', 'holahan_denise', 'wristactionblog', 'OMGGretchenL', 'roccocolantuono', 'Iwnfwya',
                'lordhelmet834', 'EyePunchNazis', 'DailyPatriot2', 'walshright', 'sharyalabluff', 'juliacusano',
                'SarahRA84', 'ScottBendure', 'FUCK15LAM', 'Thund3rStruckk', 'Maximus1901', 'Jodeecola', 'nonlynear',
                'PatrickLittle84', 'AnnaSpence15', 'RussDiBello', 'SakerPeter', 'DasTrumpnFuhrer', 'Potentialoh13th',
                'VladTheImplyer2', 'bretter66', 'gladiator1592', 'EliminateNazis', 'RoyRoss01', 'SavageMax___',
                'michaelbirdtx', '1Ron_Jewell', 'dianamday', 'schoolstreeet', 'chrisaylett', 'ProHumanDefence',
                'truthhurts4545', 'rob1031wa', 'MoniSnowflake01', 'kylei7449', 'Rob06748942', 'augustblue',
                'ThankYouForMAGA'}

    regex = re.compile("(^.*)\\s+(\\d+)\\t(.*)")
    with open(in_file, mode='r') as fhs:
        for record in fhs:
            record = record.strip()

            if regex.match(record):
                handle = regex.match(record).group(1)
                tweet = regex.match(record).group(3)

                if handle in harassers:
                    blob = TextBlob(tweet)
                    print(handle, blob.words.lower(), tweet)

    return


if __name__ == '__main__':
    """
    :param doc: path and filename where document resides       
    """

    # record running time
    start = time()
    print('Starting Time: %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))

    # checks if path was passed as an argument
    if len(sys.argv) < 2:
        print('Usage: python3 HarasserTerms.py <input_file>')
        sys.exit(-1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print('\nCould not file: %s' % input_file)
        print('Usage: python3 HarasserTerms.py <input_file>')
        sys.exit(-1)

    get_tweets(input_file)

    print('\nEnd Time:  %s' % strftime("%a,  %b %d, %Y at %H:%M:%S", localtime()))
    print('Execution Time: %.2f seconds' % (time()-start))
sys.exit(0)
