import argparse
import os
from translate_subtitles import translate_subtitles

argmap = {
  '--format': {
    'required': True,
    'help': 'Subtitle format, one of "srt", "vtt", "dfxp"'
  },
  '--input-file': {
    'required': True,
    'help': 'Full path to input subtitle file'
  },
  '--output-file': {
    'required': True,
    'help': 'Full path to output subtitle file'
  },
  '--source_language': {
    'required': True,
    'help': 'Source language code'
  },
  '--target_language': {
    'required': True,
    'help': 'Target language code'
  },
  '--cache-db-filename': {
    'required': False,
    'default': 'translate-cache.db',
    'help': 'Full path to cache database (default: %(default)s)'
  }
}

parser = argparse.ArgumentParser()
for arg, kwargs in argmap.items():
    parser.add_argument(arg, **kwargs)

args = parser.parse_args()

os.environ['TRANSLATE_CACHE_DB_FILENAME'] = args.cache_db_filename

translate_subtitles(args.format, args.input_file, args.source_language, args.output_file, args.target_language)