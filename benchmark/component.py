class Component(object):
    """docstring for Component"""
    def __init__(self):
        super(Component, self).__init__()
        self.options = {}

    def add_arguments(self, parser):
        pass

    def set_options(self, options):
        self.options = options

    def _get(self, attribute):
        if self.options.has_key(attribute):
            return self.options[attribute]
        elif hasattr(self, attribute):
            return getattr(self, attribute)
        else:
            assert False, '{} not found.'.format(attribute)

    def _has(self, attribute):
        try:
            return bool(self._get(attribute))
        except:
            return False