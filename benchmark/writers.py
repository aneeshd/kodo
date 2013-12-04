from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
from component import Component

import os

def mkdir(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


class FileWriter(Component):
    """docstring for FileWriter"""
    def __init__(self):
        super(FileWriter, self).__init__()

    def add_arguments(self, parser):
        parser.add_argument('--output-dir',
            action  = 'store',
            default = 'figures',
            help    = 'The output directory for storing the generated plots.')
        parser.add_argument('--output-format',
            action  = 'store',
            choices = ['eps', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg',
                       'svgz'],
            default = 'eps',
            help    = 'The format of the generated figures.')

    def init(self):
        mkdir(os.path.join(self._get('output_dir'), self._get('run_name')))
        pyplot.close('all')

    def save(self, name):
        pyplot.savefig(os.path.join(
            self._get('output_dir'), self._get('run_name'), '{}.{}'.format(
            name, self._get('output_format'))))

    def close(self):
        pass

class PdfWriter(Component):
    """docstring for PdfWriter"""
    def __init__(self):
        super(PdfWriter, self).__init__()

    def add_arguments(self, parser):
        parser.add_argument('--pdf-output-dir',
            action  = 'store',
            default = 'figures',
            help    = 'The output directory for storing a pdf containing all'
                      'plots.')

    def init(self):
        mkdir(os.path.join(self._get('pdf_output_dir'), self._get('run_name')))
        self.pdf = PdfPages(
            os.path.join(
                self._get('pdf_output_dir'),
                self._get('run_name'),
                'all.pdf'))

    def save(self, name):
        self.pdf.savefig(transparent = True)

    def close(self):
        self.pdf.close()
