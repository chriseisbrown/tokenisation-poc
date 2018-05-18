# !/usr/bin/env python3
import boto3
from sqlbuilders.PartitionBuilder import PartitionBuilder



AWS_PROFILE_NAME = 'ctm-data-prod'
S3_OUTPUT_LOCATION = 's3://aws-athena-query-results-077201780497-eu-west-1/data-grip/'

query_string ='select product, event_type, year, month, day, count(*)  as "events" from chrisb_dev.event_sink group by product, event_type, year, month, day order by product, event_type, day;'
database = 'chrisb_dev'


def make_partitions():
    """
        Make a list of ALTER TABLE statements to add partitions for an Athena table
        :return: list of statements
    """
    #products = ['Bike','Car','Van','Home','Travel','Mobile','Other']
    products = ['Other']
    event_types = ['ClaimOrderCreatedEvent']
    days = ['01','02','03','04','05']
    months = ['05']
    years = ['2018']

    partition_queries = []
    for product in products:
        for event in event_types:
            for year in years:
                for month in months:
                    for day in days:
                        partition_queries.append(PartitionBuilder('chrisb_dev',
                                                             'event_sink', product, event,
                                                             year, month, day, 's3://ctm-bi-eventsink', '/eventsink/'))
    return partition_queries



def run_query(client, query, database, s3_output):
    print('Executing: {query_string}'.format(query_string=query))
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

    for query in make_partitions():
        response = run_query(client, query.get_query_string(), database, S3_OUTPUT_LOCATION)
    print('Completed')


if __name__ == "__main__":
    main()