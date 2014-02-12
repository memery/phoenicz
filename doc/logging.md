Logging
=======

The logging system i Phoenicz is actually very simple. There is only *one*
function that you should use. Ever. `log(log_type, message)`.


## Basic concept

The logger is supposed to be used in all sorts of logging-scenarios, from
only *one* function. This makes it very easy to use and disables many weird
bugs.

`log(log_type, message)` takes two arguments (obviously), The type of
message you want to log and the message itself. `log_type` is
basically the same as the file you want to save the message to, i.e. a
`log_type` of `foo` will print the message to `log/foo.log` and `bar` to
`log/bar.log` and so on.

`log()` will also add some useful information such as which module called
log() along with the time and date.

In case of some errors (more specifically those occurred due to uncaught exceptions), `log()`
will also add line number, file name and what exception it was that occurred.


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

  A. An uncaught exception has occurred  
  B. No exception has occurred


### Explaination

In case of `A`, `error_info()` will add some useful information to the
log-message, such as on what line and in what function and file the exception
occurred. In `B`-case, the message will be unchanged.
