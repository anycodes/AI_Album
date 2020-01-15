# -*- coding: utf8 -*-

import yaml
import os


def setEnv():
    file = open("/Users/dfounderliu/Documents/code/AIAlbum/serverless.yaml", 'r', encoding="utf-8")
    file_data = file.read()
    file.close()

    data = yaml.load(file_data)
    for eveKey, eveValue in data['Conf']['inputs'].items():
        print(eveKey, eveValue)
        os.environ[eveKey] = str(eveValue)
