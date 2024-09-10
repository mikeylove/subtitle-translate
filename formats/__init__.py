from .srt import SrtHandler
from .vtt import VttHandler
from .dfxp import DfxpHandler

class FormatHandler:
  def __init__(self, input_file, output_file):
    self.input_file = input_file
    self.output_file = output_file

  def for_format(self, format):
    if format not in format_handlers:
      raise ValueError(f'Unsupported format: {format}')
    
    return format_handlers.get(format).get('handler')(self)
  
  def read(self):
    with open(self.input_file, 'r') as f:
      return f.read()
  
  def write(self, content):
    with open(self.output_file, 'w') as f:
      f.write(content)

format_handlers = {
  'srt': {
    'extension': '.srt',
    'handler': SrtHandler
  },
  'vtt': {
    'extension': '.vtt',
    'handler': VttHandler
  },
  'dfxp': {
    'extension': '.dfxp',
    'handler': DfxpHandler
  }
}
