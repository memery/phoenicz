Logging
=======

The logging system i Phoenicz is actually very simple. There is only *one*
function that you should use. Ever. `log(log_type, message)`.


## Basic concept

The logger is supposed to be used in all sorts of logging-scenarios, from
only *one* function. This makes it very easy to use and disables many weird
bugs.

`log(log_type, message)` takes two arguments (obviously), The type of
log-message you want to log and the message it self. `log_type` is
basically the same as the logfile you want to save the message to, i.e. a
`log_type` of `foo` will print the message to `log/foo.log` and `bar` to
`log/bar.log` and so on.

`log()` will also add some useful information such as which module called
log() and the time and date.

In case of some error (those occured due to uncatched exceptions), `log()`
will also add line number, filename and what exception it was that occured.


## Flowchart

     ---------------       -------
    | Some function | --> | log() |
     ---------------       -------
                              |
                              v
                        -------------- 
                       | error_info() | ---
                        --------------     |
                              |            |
                             [A]          [B]
                              |            |
                              v            |
     ---------------       -------         |
    | append_file() | <-- | str() | <------
     ---------------       -------

### Definitions

  A. An uncatched exception has occured  
  B. No exception has occured


### Explaination

In case of `A`, `error_info()` will add some useful information to the
log-message, such as on what line and in what function and file the exception
occured. In `B`-case, the message will be unchanged.
