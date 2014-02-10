
import errno
import json
import re
import os.path
import traceback


def read_file_or_die(fn):
    with open(fn, encoding='utf-8') as f:
        return f.read()

def read_file(fn):
    """ Read a file and return the raw data. Create a new file if necessary. """
    try:
        read_file_or_die(fn)
    except IOError as e:
        # If the file doesn't exist (that's errno.ENOENT)
        if e.errno == errno.ENOENT:
            with open(fn, mode='w', encoding='utf-8') as f:
                f.write('')
            return ''
        else:
            raise

def read_json(str):
    return json.loads(str)

def read_config(fn):
    conf = read_json(read_file_or_die(fn))
    return conf

def error_info(error):
    """
    Return a useful string containing info about the current exception.
    This should always be used when handling the exception yourself instead
    of letting irc.py do it. Without this, no line numbers!

    error is the exception that was catched
    """
    errortype = str(type(error))[8:-2]
    if not isinstance(error, BaseException):
        return 'Error in error_info: {} is type {}, not an exception'\
               ''.format(repr(error), errortype)
    exception_re = re.compile(r'File "(.+?)", line (\d+), (.+?)(\n|$)')
    try:
        stacktrace = traceback.format_exc()
        chunks = exception_re.findall(stacktrace)
        # This does not seem to work
        # errortype = stacktrace.split('\n')[-2]
    except Exception as e:
        tb = 'Error when getting stacktrace: {}'.format(e)
    else:
        if chunks:
            # [example]: file.py:38 in lolfunction
            tb = '{}:{} {}'.format(os.path.basename(chunks[-1][0]),
                                   chunks[-1][1], chunks[-1][2])
    args = (errortype, error, tb)
    return '[{}] {} - {}'.format(*args)
