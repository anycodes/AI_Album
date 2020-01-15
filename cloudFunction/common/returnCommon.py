# -*- coding: utf8 -*-

import uuid


def return_msg(error, msg):
    return_data = {
        "uuid": str(uuid.uuid1()),
        "error": error,
        "message": msg
    }
    return return_data
