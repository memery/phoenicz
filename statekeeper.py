import inspect
import os.path


class StateKeeper():
    def __init__(self):
        self.__data = {}
        self.__shared = {}#__SharedState()

    @property
    def shared(self):
        return self.__shared

    def __getitem__(self, key):
        return self.__data[self.__get_caller()][key]

    def __setitem__(self, key, value):
        caller_id = self.__get_caller()
        if caller_id not in self.__data:
            self.__data[caller_id] = {}
        self.__data[self.__get_caller()][key] = value

    def __delitem__(self, key):
        del self.__data[self.__get_caller()][key]

    def __contains__(self, key):
        return key in self.__data[self.__get_caller()]

    def _caller_id(self):
        """ Convenience function to figure out your own id """
        return self.__get_caller()

    def __get_caller(self):
        """ Return the path to the module that called the StateKeeper """
        return inspect.stack()[2][1]
