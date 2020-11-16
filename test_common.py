import unittest
import json
import os
import common


class TestCommons(unittest.TestCase):
    def test_isolate_data_regular(self):
        input_data = [{
                "id": "c1",
                "type": "corporate",
                "tenor": "10.3 years",
                "yield": "5.30%",
                "amount_outstanding": 1200000
            },
            {
                "id": "g1",
                "type": "government",
                "tenor": "9.4 years",
                "yield": "3.70%",
                "amount_outstanding": 2500000
            },
            {
                "id": "c2",
                "type": "corporate",
                "tenor": "13.5 years",
                "yield": None,
                "amount_outstanding": 1100000
            },
            {
                "id": "g2",
                "type": "government",
                "tenor": "12.0 years",
                "yield": "4.80%",
                "amount_outstanding": 1750000
            }
        ]
        corporates_expected = {
            'c1': {'amount_outstanding': 1200000, 'yield': 5.3, 'tenor': 10.3}}
        governments_expected = {'g2': {'amount_outstanding': 1750000, 'yield': 4.8, 'tenor': 12.0},
                                'g1': {'amount_outstanding': 2500000, 'yield': 3.7, 'tenor': 9.4}}
        corporate_actual, governments_actual = common.isolate_data(input_data)
        self.assertDictEqual(corporates_expected, corporate_actual, "EXPECTED " +
                             str(corporates_expected) + " GOT " + str(corporate_actual))
        self.assertDictEqual(governments_expected, governments_actual, "EXPECTED " +
                             str(governments_expected) + " GOT " + str(governments_actual))

    def test_isolate_data_no_corporate(self):
        input_data = [{
                "id": "g1",
                "type": "government",
                "tenor": "9.4 years",
                "yield": "3.70%",
                "amount_outstanding": 2500000
            },
            {
                "id": "g2",
                "type": "government",
                "tenor": "12.0 years",
                "yield": "4.80%",
                "amount_outstanding": 1750000
            }
        ]
        corporates_expected = {}
        governments_expected = {'g2': {'amount_outstanding': 1750000, 'yield': 4.8, 'tenor': 12.0},
                                'g1': {'amount_outstanding': 2500000, 'yield': 3.7, 'tenor': 9.4}}
        corporate_actual, governments_actual = common.isolate_data(input_data)
        self.assertDictEqual(corporates_expected, corporate_actual, "EXPECTED " +
                             str(corporates_expected) + " GOT " + str(corporate_actual))
        self.assertDictEqual(governments_expected, governments_actual, "EXPECTED " +
                             str(governments_expected) + " GOT " + str(governments_actual))

    def test_isolate_data_bad_government_data(self):
        input_data = [{
                "id": "c1",
                "type": "corporate",
                "tenor": "10.3 years",
                "yield": "5.30%",
                "amount_outstanding": 1200000
            },
            {
                "id": "g1",
                "type": "government",
                "tenor": None,
                "yield": "3.70%",
                "amount_outstanding": 2500000
            },
            {
                "id": "c2",
                "type": "corporate",
                "tenor": "13.5 years",
                "yield": None,
                "amount_outstanding": 1100000
            },
            {
                "id": None,
                "type": "government",
                "tenor": "12.0 years",
                "yield": "4.80%",
                "amount_outstanding": 1750000
            }
        ]
        corporates_expected = {
            'c1': {'amount_outstanding': 1200000, 'yield': 5.3, 'tenor': 10.3}}
        governments_expected = {}
        corporate_actual, governments_actual = common.isolate_data(input_data)
        self.assertDictEqual(corporates_expected, corporate_actual, "EXPECTED " +
                             str(corporates_expected) + " GOT " + str(corporate_actual))
        self.assertDictEqual(governments_expected, governments_actual, "EXPECTED " +
                             str(governments_expected) + " GOT " + str(governments_actual))
    
    def test_spread_data_regular(self):
        governments = {'g2': {'amount_outstanding': 1750000, 'yield': 4.8, 'tenor': 12.0},
                       'g1': {'amount_outstanding': 2500000, 'yield': 3.7, 'tenor': 9.4}}
        
        corporates = {'c1': {'amount_outstanding': 1200000, 'yield': 5.3, 'tenor': 10.3}}
        expected = [{
		    "corporate_bond_id": "c1",
		    "government_bond_id": "g1",
		    "spread_to_benchmark": "160 bps"
	    }] 
        actual = common.spread_data(corporates,governments)
        self.assertListEqual(expected, actual, "EXPECTED " + str(expected) + " GOT " + str(actual))
    
    def test_spread_data_more_corporations(self):
        governments = {'g2': {'amount_outstanding': 1750000, 'yield': 4.8, 'tenor': 12.0},
                       'g1': {'amount_outstanding': 2500000, 'yield': 3.7, 'tenor': 9.4}}
        
        corporates = {'c1': {'amount_outstanding': 1200000, 'yield': 5.3, 'tenor': 10.3},
                      'c2': {'amount_outstanding': 1200000, 'yield': 5.3, 'tenor': 10.3}
        }
        expected = [{
		    "corporate_bond_id": "c1",
		    "government_bond_id": "g1",
		    "spread_to_benchmark": "160 bps"
            },
            {
		    "corporate_bond_id": "c2",
		    "government_bond_id": "g1",
		    "spread_to_benchmark": "160 bps"
            },
            {
		    "corporate_bond_id": "c3",
		    "government_bond_id": "g1",
		    "spread_to_benchmark": "160 bps"
	        }
        ] 
        actual = common.spread_data(corporates,governments)
        self.assertTrue(expected[0] in actual, "EXPECTED " + str(expected) + " GOT " + str(actual))
        self.assertTrue(expected[1] in actual, "EXPECTED " + str(expected) + " GOT " + str(actual))
        self.assertTrue(expected[2] not in actual, "EXPECTED " + str(expected) + " GOT " + str(actual))

    def test_spread_data_empty_corporates(self):
        governments = {'g2': {'amount_outstanding': 1750000, 'yield': 4.8, 'tenor': 12.0},
                       'g1': {'amount_outstanding': 2500000, 'yield': 3.7, 'tenor': 9.4}}
        corporates = {}
        expected = [] 
        actual = common.spread_data(corporates,governments)
        self.assertListEqual(expected, actual, "EXPECTED " + str(expected) + " GOT " + str(actual))

    def test_spread_data_empty_governments(self):
        governments = {}
        corporates = {'c1': {'amount_outstanding': 1200000, 'yield': 5.3, 'tenor': 10.3}}
        expected = [] 
        actual = common.spread_data(corporates,governments)
        self.assertListEqual(expected, actual, "EXPECTED " + str(expected) + " GOT " + str(actual))

    def test_main_regular(self):
        args = ['common.py', 'sample_input.json', 'out.json']
        res = common.main(args)
        with open('sample_output.json') as f:
            expected = json.loads(f.read())
        with open('out.json') as f:
            actual = json.loads(f.read())
        os.remove('out.json')
        self.assertDictEqual(expected, actual, "EXPECTED " + str(expected) + " GOT " + str(actual))
        self.assertEqual(res, 0, "EXPECTED 0 GOT "+ str(res))

    def test_main_cant_open_file(self):
        args = ['common.py', 'input.json', 'out.json']
        try:
            common.main(args)
            assert False, "error should have occured"
        except:
            self.assertTrue(True)
    
    def test_main_bad_input_arguments(self):
        args = ['common.py', 'sample_input.json']
        actual = common.main(args)
        self.assertEqual(actual, 1, "EXPECTED 1 GOT " + str(actual)) 

if __name__ == "__main__":
    unittest.main()
