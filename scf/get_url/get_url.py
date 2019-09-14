# -*- coding: utf8 -*-

def main_handler(event, context):
    return {
        "url": event['queryString']['url']
    }
