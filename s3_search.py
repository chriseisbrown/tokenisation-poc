# !/usr/bin/env python3
import os
import boto3
import botocore

"""
Module Docstring
"""

AWS_PROFILE_NAME = 'ctm-data-nonprod'
S3_BUCKET_NAME = 'ctm-bi-release-nonprod'

S3_OBJECT_PREFIX = 'ModelTransformation/'
S3_OBJECT_FILE_NAME = 'inputSource.json'

LOCAL_PATH = '/Users/chrisb/development/python/tokenisation-poc/data/'



def main():
    """ Main entry point of the app
        Find objects in S3 bucket that contain a prefix and are a particular object file name
    """
    session = boto3.Session(profile_name=AWS_PROFILE_NAME )
    s3 = session.resource('s3')

    my_bucket = s3.Bucket(S3_BUCKET_NAME)

    for object_summary in my_bucket.objects.filter(Prefix=S3_OBJECT_PREFIX):
        key_name = str(object_summary.key)
        if S3_OBJECT_FILE_NAME in key_name:
            print('{0} : {1}'.format(my_bucket.name, object_summary.key))
            local_object_name= LOCAL_PATH + key_name

            print(local_object_name)
            try:
                make_directory(build_directory_name(local_object_name))

                s3.Bucket(S3_BUCKET_NAME).download_file(object_summary.key, local_object_name)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    print(e)

    print('Done')


def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item):
            return item


def build_directory_name(local_name):
    file_name_index = local_name.find(S3_OBJECT_FILE_NAME)
    file_object_index = local_name.find(S3_OBJECT_PREFIX)
    dir_name = LOCAL_PATH + local_name[file_object_index: file_name_index-1]
    return dir_name


def make_directory(dir_name):
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except OSError as e:
        print(e)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()