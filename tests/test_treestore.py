from unittest import TestCase
from copy import deepcopy

from treestore import TreeStore


test_items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]

class TestTreeStore(TestCase):
    def setUp(self):
        # TreeStore mutates the original input, still is's only
        # needed for testing purposes, so we create a copy of it.
        items = deepcopy(test_items)
        self.ts = TreeStore(items=items)

    def test_getAll(self):
        result = self.ts.getAll()
        self.assertEqual(test_items, result)

    def test_getItem(self):
        for original_item in test_items:
            result = self.ts.getItem(original_item["id"])
            self.assertEqual(original_item, result)

    def test_getChildren(self):
        result = self.ts.getChildren(4)
        expected = [{"id":7,"parent":4,"type":None},{"id":8,"parent":4,"type":None}]
        self.assertEqual(expected, result)

    def test_getAllParents(self):
        result = self.ts.getAllParents(7)
        expected = [{"id":4,"parent":2,"type":"test"},{"id":2,"parent":1,"type":"test"},{"id":1,"parent":"root"}]
        self.assertEqual(expected, result)
        
