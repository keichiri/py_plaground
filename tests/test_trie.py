import unittest
import time
import random
from copy import copy

from playground.trie import Trie


class TrieTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        random.seed(time.time())
        with open('/usr/share/dict/words') as f:
            content = f.read()

        cls.test_input = {}
        for word in content.split('\n'):
            value = sum(ord(c) for c in word)
            if word and word not in cls.test_input:
                cls.test_input[word] = value

    def test_building(self):
        input_data = copy(self.test_input)
        all_keys = list(input_data.keys())
        random.shuffle(all_keys)
        chosen_keys = all_keys[:len(all_keys) // 10]

        not_added_test_data = {}
        for key in chosen_keys:
            value = input_data.pop(key)
            not_added_test_data[key] = value

        trie = Trie(input_data)

        self.assertEqual(trie.size, len(input_data))
        for key, value in input_data.items():
            self.assertEqual(trie.get(key), value)

        for key, value in not_added_test_data.items():
            self.assertEqual(trie.get(key), None)

        all_in_trie = list(iter(trie))
        all_in_trie.sort(key=lambda x: x[0])

        input_data = [(k, v) for k, v in input_data.items()]
        input_data.sort(key=lambda x: x[0])

        self.assertEqual(input_data, all_in_trie)

    def test_building_and_removing(self):
        input_data = copy(self.test_input)
        all_keys = list(input_data.keys())
        random.shuffle(all_keys)
        chosen_keys = all_keys[:len(all_keys) // 10]

        not_added_test_data = {}
        for key in chosen_keys:
            value = input_data.pop(key)
            not_added_test_data[key] = value

        trie = Trie(input_data)

        self.assertEqual(trie.size, len(input_data))
        for key, value in input_data.items():
            self.assertEqual(trie.get(key), value)

        existing_keys = list(input_data.keys())
        random.shuffle(existing_keys)
        to_remove = existing_keys[:len(existing_keys) // 3]
        for key in to_remove:
            input_data.pop(key)

        for key in to_remove:
            trie.remove(key)

        self.assertEqual(trie.size, len(input_data))

        for key in to_remove:
            self.assertIsNone(trie.get(key))

        for key, value in input_data.items():
            self.assertEqual(trie.get(key), value)

        for key, value in not_added_test_data.items():
            self.assertIsNone(trie.get(key))

        all_in_trie = list(iter(trie))
        all_in_trie.sort(key=lambda x: x[0])

        input_data = [(k, v) for k, v in input_data.items()]
        input_data.sort(key=lambda x: x[0])

        self.assertEqual(input_data, all_in_trie)