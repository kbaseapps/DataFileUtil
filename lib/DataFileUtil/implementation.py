# contains implementations for DFU methods. This allows for unit testing.

# hmm, class or functions, class or functions... let's go with functions for now.
# If we wind up having to pass in a ton of crap every time try an OO approach.

# TODO move more method implementations here - or in other files - as needed.
# TODO mypy this sucker up

import copy
import time

from installed_clients.baseclient import ServerError as WorkspaceError


def log(message, prefix_newline=False):
    print(('\n' if prefix_newline else '') + str(time.time()) + ': ' + str(message))

# Copies of this in AssemblyUtil and GenomeFileUtil may be redundant since we're sorting here
# Note that insertion order is only maintained since python 3.6 and is only guaranteed since 3.7
# In 3.6 it was an implementation detail.
# As of 2020/12/12 Python 3.6 is provided in the kbase/sdkbase2 image
def _sort_dict(in_struct):
    """
    Recursively sort a dictionary by dictionary keys.
    """
    if isinstance(in_struct, dict):
        return {k: _sort_dict(in_struct[k]) for k in sorted(in_struct)}
    elif isinstance(in_struct, list):
        return [_sort_dict(k) for k in in_struct]
    else:
        return in_struct


def save_objects(ws, params, prov):
    # TODO unit tests
    objs = params.get('objects')
    if not objs:
        raise ValueError('Required parameter objects missing')
    wsid = params.get('id')
    if not wsid:
        raise ValueError('Required parameter id missing')
    objs_to_save = []
    for o in objs:
        obj_to_save = {}

        prov_to_save = prov
        if 'extra_provenance_input_refs' in o:
            # need to make a copy so we don't clobber other objects
            prov_to_save = copy.deepcopy(prov)
            extra_input_refs = o['extra_provenance_input_refs']
            if extra_input_refs:
                if len(prov) > 0:
                    if 'input_ws_objects' in prov[0]:
                        prov_to_save[0]['input_ws_objects'].extend(extra_input_refs)
                    else:
                        prov_to_save[0]['input_ws_objects'] = extra_input_refs
                else:
                    prov_to_save = [{'input_ws_objects': extra_input_refs}]

        keys = ['type', 'name', 'objid', 'meta', 'hidden']
        for k in keys:
            if k in o:
                obj_to_save[k] = o[k]
        """
        Sorting the data is important for 2 reasons:
        1) It prevents the workspace from rejecting the save because the sort takes too much memory.
           The workspace puts limits on memory use because it has to service many apps / UIs / etc.
           at once.
        2) It distributes the sort across the app worker nodes rather than concentrating them on
           the workspace node.
        """
        # TODO sort in WSLargeDataIO as well
        if 'data' in o:
            obj_to_save['data'] = _sort_dict(o['data'])

        obj_to_save['provenance'] = prov_to_save
        objs_to_save.append(obj_to_save)

    try:
        return ws.save_objects({'id': wsid, 'objects': objs_to_save})
    except WorkspaceError as e:
        log('Logging workspace error on save_objects: {}\n{}'.format(e.message, e.data))
        raise
