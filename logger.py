import inspect, datetime
import common

def log(message, type, test=False):
    frames = inspect.stack()[1]
    mod = inspect.getmodule(frames[0])

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    filename = 'log/{}.log'.format(type)
    msg = '{} [{}]: {}'.format(mod.__name__, ts, message)

    if not test:
        append_file(filename, msg)
        return None
    else:
        return { 'filename': filename,
                 'msg': msg }
