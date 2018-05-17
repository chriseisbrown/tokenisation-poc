import os
from os import listdir
from os.path import isfile, join
import configparser
import argparse
import json
from pprint import pprint

"""
    Inspects a folder of .json event schema and tries to match words form the config.ini file
    in the body of teh schems.  Used to try and find PII fields in the schema.
"""

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
    print('Reading config variables')
    # set up config variables
    import_config(search_terms)

    key_words = search_terms[KEY_WORDS]
    print('Looking for these words: {}'.format(key_words))
    key_words = key_words.split(',')

    command_args = parse_args()
    search_folder = command_args['folder']
    print('Looking in folder ({folder_name}) for tokenisable values'.format(folder_name = search_folder))

    file_names = []
    full_file_path = []

    for root, dir, files in os.walk(search_folder):
        if not dir:
            for file in files:
                full_file_path.append(root + '/' + file)
                file_names.append(file)

    total_files = len(full_file_path)
    print('Found {} files to check'.format(total_files))

    found_count = 0
    found_in_file_paths = []
    found_in_file_name = []

    for file_path in full_file_path:
        print('Checking file {}'.format(file_path))
        with open(file_path) as json_data:
            schema = json.load(json_data)
            # json into string format
            payload = json.dumps(schema)
            if any(keyword in payload.lower() for keyword in key_words):
                print('Found keyword in schema!')
                found_count += 1
                found_in_file_paths.append(file_path)
                found_in_file_name.append(file_names[full_file_path.index(file_path)])
                # tell me the specific key word found
                for keyword in key_words:
                    if keyword in payload.lower():
                        print('Found {}'.format(keyword))

    print('Found keywords in {} of {} files'.format(found_count, total_files))
    # full file path
    pprint(found_in_file_paths)
    # just the file name part
    pprint(found_in_file_name)


if __name__ == "__main__":
    main()

