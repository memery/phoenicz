
import common
import irc


def main():
    settings = common.read_config('config')
    # TODO: Validate settings (and give helpful
    # error messages if they are invalid)
    # (Could probably be a method in common)

    while True:
        if irc.run(settings) == 'quit':
            break
        sleep(settings['irc']['reconnect_delay'])


if __name__ == '__main__':
    main()

