# unit tests for the implementation.py file.

import json

from unittest.mock import create_autospec

from installed_clients.WorkspaceClient import Workspace

from DataFileUtil.implementation import save_objects

# TODO add more save_object unit tests.
# TODO upgrade to pytest.
# TODO figure out why the test results are interleaved with test logs & fix
# TODO figure out why there appear to be 2 test runs, 1 with this file, 1 without, per kb-sdk test
# TODO set up a makefile target to run only unit tests

def test_save_objects_sorted():
    print("***** test_save_objects_sorted ****")
    ws = create_autospec(Workspace, spec_set=True, instance=True)

    ws.save_objects.return_value = [
        [
            17,
            'objname',
            'Some.Type-2.4',
            '2020-12-12T19:52:29+0000',
            2367,
            'username',
            49778,
            'MyWorkspace',
            '99914b932bd37a50b983c5e7c90ae93b',
            2,
            {}],
        [
            18,
            'objname2',
            'Other.Type-2.4',
            '2020-12-12T19:52:29+0000',
            1,
            'username',
            49778,
            'MyWorkspace',
            '99914b932bd37a50b983c5e7c90ae93b',
            2,
            {}]
        ]
    
    params = {
        'id': 49778,
        'objects': [
            {
             'type': 'Some.Type-2.4',
             'name': 'objname',
             'data': {'sorted': [
                         3,
                         2,
                         1, 
                         {
                             '4': 'a',
                             '3': 'a',
                             '1': 'a',
                             '2': 'a'
                          }],
                      'by': 1,
                      'yoda': ['whoo', 'whee', {'b': 1, 'a': 2}],
                      'this was': 'foo'}
            },
            {
             'type': 'Other.Type-2.4',
             'name': 'objname2',
             'data': {
                'a': 1,
                'c': 2,
                'b': 3,
                }
            }]
    }

    res = save_objects(ws, params, {})
    expected = [
        [
            17,
            'objname',
            'Some.Type-2.4',
            '2020-12-12T19:52:29+0000',
            2367,
            'username',
            49778,
            'MyWorkspace',
            '99914b932bd37a50b983c5e7c90ae93b',
            2,
            {}],
        [
            18,
            'objname2',
            'Other.Type-2.4',
            '2020-12-12T19:52:29+0000',
            1,
            'username',
            49778,
            'MyWorkspace',
            '99914b932bd37a50b983c5e7c90ae93b',
            2,
            {}]
        ]
    assert res == expected

    ws.save_objects.assert_called_once_with({
        'id': 49778,
        'objects': [
            {
             'type': 'Some.Type-2.4',
             'name': 'objname',
             'data': {'sorted': [
                         3,
                         2,
                         1, 
                         {
                             '4': 'a',
                             '3': 'a',
                             '1': 'a',
                             '2': 'a'
                          }],
                      'by': 1,
                      'yoda': ['whoo', 'whee', {'b': 1, 'a': 2}],
                      'this was': 'foo'
                      },
             'provenance': {}
             },
            {
             'type': 'Other.Type-2.4',
             'name': 'objname2',
             'data': {
                'a': 1,
                'c': 2,
                'b': 3,
                },
             'provenance': {}
            }]
        })

    assert json.dumps(ws.save_objects.call_args[0][0]['objects'][0]['data']) == (
        '{"by": 1, "sorted": [3, 2, 1, {"1": "a", "2": "a", "3": "a", "4": "a"}], ' +
        '"this was": "foo", "yoda": ["whoo", "whee", {"a": 2, "b": 1}]}'
    )

    assert json.dumps(ws.save_objects.call_args[0][0]['objects'][1]['data']) == (
        '{"a": 1, "b": 3, "c": 2}'
    )
