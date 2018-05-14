import os
import configparser
import argparse


search_terms = {}
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

    print(search_terms['words'])
    print(search_terms['attempts'])

    command_args = parse_args()
    print('Looking in folder ({folder_name}) for tokenisable values'.format(folder_name = command_args['folder']))


if __name__ == "__main__":
    main()
