## Command line-based translation for various subtitle formats.

```
usage: translate.py [-h] --format FORMAT --input-file INPUT_FILE --output-file OUTPUT_FILE --source_language SOURCE_LANGUAGE --target_language TARGET_LANGUAGE
                    [--cache-db-filename CACHE_DB_FILENAME]

options:
  -h, --help            show this help message and exit
  --format FORMAT       Subtitle format, one of "srt", "vtt", "dfxp"
  --input-file INPUT_FILE
                        Full path to input subtitle file
  --output-file OUTPUT_FILE
                        Full path to output subtitle file
  --source_language SOURCE_LANGUAGE
                        Source language code
  --target_language TARGET_LANGUAGE
                        Target language code
  --cache-db-filename CACHE_DB_FILENAME
                        Full path to cache database (default: translate-cache.db)
```
