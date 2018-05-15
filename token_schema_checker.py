from os import listdir
from os.path import isfile, join
import configparser
import argparse
import json
from pprint import pprint



search_terms = {}
KEY_WORDS = 'search_words'
DEFAULT_FOLDER_NAME = 'data/'


def parse_args():
    '''
        Parse command line arguments
    '''
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=False, help="folder to search for tokenisable values", nargs='?')
    args = vars(ap.parse_args())
    if args['folder'] is None:
        args['folder'] = DEFAULT_FOLDER_NAME
    return args


def import_config(config_holder):
    '''
        Search terms are kept in an .ini file.  Read them into the variables

        Parameters
        ----------
        config_holder : array
            array passed in to hold the configuration variables from the .ini file
    '''
    config = configparser.ConfigParser()
    config.sections()
    config.read('config/config.ini')

    search_section = config['search']
    for key in search_section:
        config_holder[key] = search_section[key]


def main():
    print('Read config variables')
    # set up config variables
    import_config(search_terms)
    for key in search_terms:
        print(key)

    key_words = search_terms[KEY_WORDS]
    print('Looking for these words: {}'.format(key_words))
    key_words = key_words.split(',')

    command_args = parse_args()
    print('Looking in folder ({folder_name}) for tokenisable values'.format(folder_name = command_args['folder']))

    file_names = [f for f in listdir(DEFAULT_FOLDER_NAME) if isfile(join(DEFAULT_FOLDER_NAME, f))]

    for file_name in file_names:
        key_name = DEFAULT_FOLDER_NAME + file_name
        print('Checking file {}'.format(key_name))
        with open(key_name) as json_data:
            schema = json.load(json_data)

            print('Product is {}, version {}'.format(schema['productName'], schema['version']))

            # check if "body" (lowercased) contains any of the keywords
            payload = json.dumps(schema['structure'])
            if any(keyword in payload.lower() for keyword in key_words):
                print('Found keyword in schema!')
                # tell me the specific key word found
                for keyword in key_words:
                    if keyword in payload.lower():
                        print('Found {}'.format(keyword))


if __name__ == "__main__":
    main()

