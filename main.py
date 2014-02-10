
import common, logger
import irc


def valid_settings(settings, log=logger.log):
    essentials = {'irc': {
                     'nick': str,
                     'channel': str,
                     'server': str,
                     'port': int,
                     'ssl': bool,
                     'reconnect_delay': int,
                 }}

    for category in essentials:
        for setting in essentials[category]:
            try:
                setting_type = essentials[category][setting]
                if type(settings[category][setting]) != setting_type:
                    log('error', 'Invalid settings: {}/{} must be of type {}. Closing.'.format(category, setting, str(setting_type)))
                    return False
            except KeyError:
                log('error', 'Invalid settings: {}/{} not found. Closing.'.format(category, setting))
                return False

    return True


def main():
    settings = common.read_config('config')
    if not valid_settings(settings):
        exit()

    while True:
        if irc.run(settings) == 'quit':
            break
        sleep(settings['irc']['reconnect_delay'])


if __name__ == '__main__':
    main()

