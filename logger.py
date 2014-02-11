import inspect, datetime, errno, os, re, traceback

def error_info(error):
    """
    Return a useful string containing info about the current exception.
    This should always be used when handling the exception yourself instead
    of letting irc.py do it. Without this, no line numbers!

    error is the exception that was catched
    """
    errortype = str(type(error))[8:-2]
    if not isinstance(error, BaseException):
        return error
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
    msg = '{} [{}]: {}'.format(mod.__name__, ts, str(error_info(message)))

    append_file(filename, msg)

    return { 'filename': filename,
             'msg':      msg       }
