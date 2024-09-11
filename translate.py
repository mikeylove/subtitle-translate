import argparse
import os
from translate_subtitles import translate_subtitles

def is_stats_mode():
  return '--cache-stats' in os.sys.argv

argmap = {
  '--format': {
    'required': not is_stats_mode(),
    'help': 'Subtitle format, one of "srt", "vtt", "dfxp"'
  },
  '--input-file': {
    'required': not is_stats_mode(),
    'help': 'Full path to input subtitle file'
  },
  '--output-file': {
    'required': not is_stats_mode(),
    'help': 'Full path to output subtitle file'
  },
  '--source_language': {
    'required': not is_stats_mode(),
    'help': 'Source language code'
  },
  '--target_language': {
    'required': not is_stats_mode(),
    'help': 'Target language code'
  },
  '--cache-db-filename': {
    'required': False,
    'default': 'translate-cache.db',
    'help': 'Full path to cache database (default: %(default)s)'
  },
  '--cache-stats': {
    'required': False,
    'default': False,
    'action': 'store_true',
    'help': 'Print cache statistics'
  }
}

parser = argparse.ArgumentParser()
for arg, kwargs in argmap.items():
  parser.add_argument(arg, **kwargs)

args = parser.parse_args()

os.environ['TRANSLATE_CACHE_DB_FILENAME'] = args.cache_db_filename

if args.cache_stats:
  from cache import stats
  stats()
else:
  translate_subtitles(args.format, args.input_file, args.source_language, args.output_file, args.target_language)