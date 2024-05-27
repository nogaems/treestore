## Run tests


```bash
user@desktop ~/treestore (master) $ python -m unittest discover -v tests
test_getAll (test_treestore.TestTreeStore.test_getAll) ... ok
test_getAllParents (test_treestore.TestTreeStore.test_getAllParents) ... ok
test_getChildren (test_treestore.TestTreeStore.test_getChildren) ... ok
test_getItem (test_treestore.TestTreeStore.test_getItem) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK

```

## Possible improvements directions

First things that come to mind:

 - Use Pydantic for validation and serialization, that will reduce the amount of boilerplate code.
 - Provided testing samples are insuffitient for testing real-world corner cases of interacting with user input, therefore it is mandatory to use fuzzing or at least generate some more samples manually.
 - Make some measurements and collect profiling data (before doing any premature optimization).
