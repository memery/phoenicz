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

def log(type, message, output_to_file=True):
    frames = inspect.stack()[1]
    mod = inspect.getmodule(frames[0])

    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    filename = 'log/{}.log'.format(type)
    msg = '{} [{}]: {}'.format(mod.__name__, ts, message)

    if output_to_file:
        append_file(filename, msg)

    return { 'filename': filename,
             'msg':      msg       }


