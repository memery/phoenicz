import inspect, datetime, errno, os

def append_file(file, str):
    try:
        with open(file, 'a') as f:
            f.write(str + '\n')
    except IOError as e:
        if not os.path.exists('log/'):
            os.makedirs('log')

        if e.errno == errno.ENOENT:
            with open(file, 'w') as f:
                f.write(str + '\n')
        else:
            raise

def log(log_type, message):
    frames = inspect.stack()[1]
    mod = inspect.getmodule(frames[0])

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    filename = 'log/{}.log'.format(log_type)
    msg = '{} [{}]: {}'.format(mod.__name__, ts, message)

    append_file(filename, msg)

    return { 'filename': filename,
             'msg':      msg       }
