from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages


class FileWriter(object):
    """docstring for FileWriter"""
    def __init__(self):
        super(FileWriter, self).__init__()

    def add_options(self, parser):
        parser.add_option('--output-dir',
            action  = 'store',
            default = 'figures',
            help    = 'The output directory for storing the generated plots.')
        parser.add_option('--output-format'
            action  = 'store',
            choices = ['eps', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg',
                       'svgz'],
            default = 'eps',
            help    = 'The format of the generated figures.')

    def init(self, options):
        pyplot.close('all')

    def write(self, options, benchmark):
        pyplot.savefig(os.path.join(
            options['pdf_output_dir'], '{}.{}'.format(
            benchmark, options['output-format'])))

    def close(self, options):
        pass


class PdfWriter(object):
    """docstring for PdfWriter"""
    def __init__(self):
        super(PdfWriter, self).__init__()

    def add_options(self, parser):
        parser.add_option('--pdf-output-dir',
            action  = 'store',
            default = 'figures',
            help    = 'The output directory for storing a pdf containing all'
                      'plots.')

    def init(self, options):
        self.pdf = PdfPages(os.path.join(options['pdf_output_dir'], 'all.pdf'))

    def write(self, options, benchmark):
        self.pdf.savefig(transparent = True)

    def close(self, options):
        self.pdf.close()
