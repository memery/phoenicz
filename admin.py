import common
import logger

import re

def is_admin(nick, log=logger.log):
    try:
        adminlist = common.read_config('admins.json')
    except Exception as e:
        log('error', e)
        return False
    if not isinstance(adminlist, list):
        log('error', 'admins.json should contain a list')
        return False
    return nick in adminlist

def parse_admin_command(text, botnick, log=logger.log):
    if not botnick:
        log('error', 'No nick specified for me')
        return None
    result = re.search(r'^{}[:,]\s+(.+)$'.format(botnick), text)
    if not result:
        return None
    # TODO: temporary as hell as we figure out where/how to implement it all
    command = result.group(1)
    if command in ('quit', 'reload', 'restart'):
        return command
