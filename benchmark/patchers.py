class AddBuilderNamePatcher(object):
    """docstring for AddBuilderNamePatcher"""
    def __init__(self):
        super(AddBuilderNamePatcher, self).__init__()

    def add_option(parser):
        pass

    def patch(options, data_frame):
        if not data_frame['buildername']:
            data_frame['buildername'] = "local"