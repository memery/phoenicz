Functionality Architecture
==========================

The following tree diagram is meant to be read from left to right, up to down.
Since `irc` is inside of `main`, it means `main` will call functions from
`irc`, which in turn will call functions from `ircparser`, `admin` and
`behaviour` *in that order*.


    main
      |
      +---- irc
             |
             +----- ircparser
             |
             +----- admin
             |
             +----- behaviour
                        |
                        +------ plugins
                        |
                        +------ markov


