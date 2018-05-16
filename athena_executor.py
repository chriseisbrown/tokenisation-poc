# !/usr/bin/env python3
import boto3

AWS_PROFILE_NAME = 'ctm-data-prod'
S3_OUTPUT_LOCATION = 's3://aws-athena-query-results-077201780497-eu-west-1/data-grip/'

query_string ='select product, event_type, year, month, day, count(*)  as "events" from chrisb_dev.event_sink group by product, event_type, year, month, day order by product, event_type, day;'
database = 'chrisb_dev'


def run_query(client, query, database, s3_output):
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
            },
        ResultConfiguration={
            'OutputLocation': s3_output,
            }
        )
    print('Execution ID: ' + response['QueryExecutionId'])
    return response


def main():
    """
        Build and execute SQL queries on Athena
    """
    session = boto3.Session(profile_name=AWS_PROFILE_NAME )
    client = session.client('athena')
    response = run_query(client, query_string, database, S3_OUTPUT_LOCATION)
    print('Completed')


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()