
class PartitionBuilder(object):
    products = ['Bike', 'Car', 'Van', 'Home', 'Other']
    event_types = ['ClaimOrderCreatedEvent']
    days = ['01', '02', '03']
    months = ['01']
    years = ['2018']

    def __init__(self, database_name, table_name, product_name, event_name, year, month, day,  bucket, bucket_folder):
        self.query_string = 'ALTER TABLE {database_name}.{table_name} ADD PARTITION(product="{product_name}", event_type="{event_name}" ,' \
            'year="{year}",month="{month}", day="{day}") LOCATION "{bucket}/{bucket_folder}/{product_name}/{event_name}/{year}/{month}/{day}/" ;'\
            .format(database_name=database_name,
                    table_name=table_name,
                    product_name=product_name,
                    event_name=event_name,
                    year=year,
                    month=month,
                    day=day,
                    bucket=bucket,
                    bucket_folder=bucket_folder)

    def get_query_string(self):
        return self.query_string


if __name__ == "__main__":
    partition_builder = PartitionBuilder('chrisb_dev','event_sink', 'Other', 'ClaimOrderModifiedEvent',
                                         '2018', '02', '01', 's3://ctm-bi-eventsink', '/eventsink/')
    print(partition_builder.query_string)

