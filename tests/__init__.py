# -*- coding: utf-8 -*-
import os
import sys
import threading
from os import path
import nixops.statefile

_multiprocess_shared_ = True

db_file = f"{path.dirname(__file__)}/test.nixops"


def setup():
    nixops.statefile.StateFile(db_file, writable=True).close()


def destroy(sf, uuid):
    depl = sf.open_deployment(uuid)
    depl.logger.set_autoresponse("y")
    try:
        depl.clean_backups(keep=0)
    except Exception:
        pass
    try:
        depl.destroy_resources()
    except Exception:
        pass
    depl.delete()
    depl.logger.log("deployment ‘{0}’ destroyed".format(uuid))


def teardown():
    sf = nixops.statefile.StateFile(db_file, writable=True)
    uuids = sf.query_deployments()
    threads = [threading.Thread(target=destroy, args=(sf, uuid)) for uuid in uuids]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    uuids_left = sf.query_deployments()
    sf.close()
    if not uuids_left:
        os.remove(db_file)
    else:
        sys.stderr.write(
            "warning: not all deployments have been destroyed; some resources may still exist!\n"
        )
