import random
import time
import string
from locust import HttpLocust, TaskSet, task


def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date_generator(start, end, prop):
    return strTimeProp(start, end, '%Y-%m-%dT%H:%M:%SZ', prop)

def random_string_generator(size=18, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def random_email_generator():
    return random_string_generator(size=random.randint(1,20)) + "@" + random_string_generator(size=random.randint(1,10)) + ".com"


class TokenisationTaskSet(TaskSet):

    @task(1)
    def tokenisation_generate_string(self):
        random_string = random_string_generator(size=random.randint(10,50))
        print("executing tokenisation_generate_token {}".format(random_string))
        response = self.client.post("/tokenise", {"value": random_string})
        print(response.content)

    @task(1)
    def tokenisation_generate_email(self):
        random_email = random_email_generator()
        print("executing tokenisation_generate_email {}".format(random_email))
        response = self.client.post("/tokenise", {"value": random_email})
        print(response.content)

    @task(10)
    def tokenisation_generate_ISODate(self):
        random_date = random_date_generator("2008-1-1 01:30:00", "2009-1-1 04:50:00", random.random())
        print("executing tokenisation_generate_ISODate {}".format(random_date))
        response = self.client.post("/tokenise", {"value": random_date})
        print(response.content)


class TokenisationLocust(HttpLocust):
    '''
    Run this from working directory to hit the tokenisation API:
        locust --host=http://127.0.0.1:5000 -f TokenisationLocust.py
    '''
    task_set = TokenisationTaskSet
    min_wait = 2000
    max_wait = 10000