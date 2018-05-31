from TokenisationLocust import random_string_generator
from unittest import TestCase


class TokenisationLocustTest(TestCase):

    def test_default_string_length(self):
        random_string = random_string_generator()
        self.assertEqual(6, len(random_string))
