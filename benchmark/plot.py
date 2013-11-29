import argparse
import sys
from commandline_arguments import commandline_args

class Plot(object):
    """Base class for the plotting scripts"""
    def __init__(self, name, parser, cmd_args, singleton = True):
        super(Plot, self).__init__()

        self.name = name
        self.parser = parser
        self.singleton = singleton
        self.cmd_args = cmd_args

        self.__add_arguments()

    def __add_arguments(self):
        customization = {'name' : self.name}

        for arg_name in self.cmd_args:
            # enable argument customization
            cmd_arg = {}

            for name, value in commandline_args[arg_name].iteritems():
                name = name.format(**customization)
                if isinstance(value, basestring):
                    value = value.format(**customization)
                cmd_arg[name] = value
            if not self.singleton:
                arg_name = '{}-{}'.format(self.name, arg_name)
            self.parser.add_argument('--{}'.format(arg_name), **cmd_arg)

    def __parse_args(self):
        args = self.parser.parse_args(sys.argv[2:])

        result = {}
        for (key, value) in args._get_kwargs():
            key.replace('_', '-')
            if not self.singleton:
                key = key.replace('{}-'.format(self.name), '')
            if key in self.cmd_args:
                result[key] = value

        return result

    def __query(self):
        pass
    def plot(self):
        print self.__parse_args()
