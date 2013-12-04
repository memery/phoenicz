

def main():
    settings = common.read_config('config')

    while True:
        if irc.run(settings) == 'quit':
            break


if __name__ == '__main__':
    main()

