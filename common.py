
import errno
import json


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


def append_file(file, str):
    try:
        with open(file, 'a') as f:
            f.write(str)
    except IOError:
        print('Cannot write to \'{}\'. Anyway:\n{}'.format(file, str))
