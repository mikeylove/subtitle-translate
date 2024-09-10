from formats.srt import SrtHandler

PREFIX = 'WEBVTT\n\n'

class VttHandler(object):
  def __init__(self, format_handler):
    self.format_handler = format_handler
    self.srt_handler = SrtHandler(self)
    self.subtitles = list()
  
  def iterable(self):
    if len(self.subtitles) == 0:
      self._read_subtitles()
      
    return self.srt_handler.iterable()
    
  def _read_subtitles(self):
    self.subtitles_raw = self.format_handler.read().removeprefix(PREFIX)
    
  def read(self):
    return self.subtitles_raw

  def write(self):
    self.format_handler.write(self._to_vtt())
    
  def _to_vtt(self):
    return f'WEBVTT\n\n{self.srt_handler._to_srt()}'