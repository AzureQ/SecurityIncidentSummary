import unittest
import json
from src.data_processing import identity_lookup


class DataProcessingTests(unittest.TestCase):

    def setUp(self):
        """ Your setUp """
        test_data_dir = 'tests/data/'
        self.incident_types = ['other', 'denial', 'executable', 'intrusion', 'misuse', 'probing', 'unauthorized']
        self.incident_lists = []
        self.identity_lists = []
        for inc_type in self.incident_types:
            with open(test_data_dir + inc_type + '.json') as f:
                self.incident_lists.append(json.load(f))
        with open(test_data_dir + 'identity.json') as f:
            self.identity_lists.append(json.load(f))

    def test_input_setup(self):
        """ Test that the dataframe read in equals what you expect"""
        assert len(self.incident_lists) == 7
        assert len(self.incident_types) == 7
        assert len(self.identity_lists) == 1

    def test_identity_lookup(self):
        assert identity_lookup('17.20.28.45', self.identity_lists[0]) == 355684
        assert identity_lookup(355684, self.identity_lists[0]) == 355684


if __name__ == '__main__':
    unittest.main()
