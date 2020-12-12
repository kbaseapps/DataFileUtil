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

        keys = ['type', 'data', 'name', 'objid', 'meta', 'hidden']
        for k in keys:
            if k in o:
                obj_to_save[k] = o[k]

        obj_to_save['provenance'] = prov_to_save
        objs_to_save.append(obj_to_save)

    try:
        return ws.save_objects({'id': wsid, 'objects': objs_to_save})
    except WorkspaceError as e:
        log('Logging workspace error on save_objects: {}\n{}'.format(
            e.message, e.data))
        raise
