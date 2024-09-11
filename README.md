## Command line-based translation for various subtitle formats.

### Usage
```
usage: translate.py [-h] --format FORMAT --input-file INPUT_FILE --output-file OUTPUT_FILE --source_language SOURCE_LANGUAGE --target_language TARGET_LANGUAGE
                    [--cache-db-filename CACHE_DB_FILENAME] [--cache-stats]

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
  --cache-stats         Print cache statistics and quit
m```

### General Notes
- I can't speak to the accuracy of format handling, as these modules weren't designed according to a spec (lol) but rather against example exports provided to me. I might do a followup for accuracy in that regard, but am quickly approaching the "I'm bored with this" state of development so...guess we'll see. 🤷🏻‍♂️

### Format Notes

#### SRT
1) The outermost formatting tags will be retained, with their contents replaced by a translation against the block of text with inner tags stripped out (ie, in "this <b>block</b> of text", the bold tags would be removed). This is done on the [possibly] faulty assumption that translating a larger chunk of text will yield a better result than little bits translated sequentially.

#### VTT
1) Having been developed based on some sample subtitle exports, near as I can tell this is just SRT with a header (`WEBVTT\n\n`), so it utilizes the SRT module under the hood.

#### DFXP
1) XML is a funny beast. Compound subtitle entries (multiple lines separated by self-closing `br` tags) hierarchically are chains of elements with children and tail/text nodes. Yeah, I don't really fully get it either.

### Translation Engine Notes
- The code currently uses the python module `translators`, and inside of that the `google` interface. I think this queries against Google Translate? Not sure, but it didn't require any kind of API key or registration, which was pretty great. Who wants to think about that kind of stuff?

### Caching
- The code uses `sqlite3` to maintain a database of previous translations. This provides a nice speedup in the case of making editorial changes to input subtitle sources. Queries of the same content against the same engine/backend combination (currently hardcoded as `translators-google`) will check this cache before attempting a new translation.