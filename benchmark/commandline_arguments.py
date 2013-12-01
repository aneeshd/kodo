# Dest will be generated based on the
commandline_args = {
    'coder' : {
        'action'  : 'store',
        'choices' : ['encoder', 'decoder'],
        'default' : 'decoder',
        'help'    : 'Whether to consider the encoding or decoding performance.'
    },
    'days' : {
        'action'  : 'store',
        'default' : 3,
        'help'    : 'How many days to look back in time when comparing.',
        'type'    : int
    },
}

#verify command line args
for arg in commandline_args:
    for option in commandline_args[arg]:
        assert option != 'dest', \
            '"dest" should not be defined manually. It was in {}.'.format(arg)