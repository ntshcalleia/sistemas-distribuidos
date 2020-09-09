import json, os, re, collections

CACHE_FILE = os.path.join("database", "cache.json")

def process(file = str, n = 10):
    """Return n most frequent words inside file, as well as their count"""
    cache = get_cache()
    file_path = os.path.join("database", file)
    if file in cache and cache[file]["mtime"] == os.path.getmtime(file_path): # if file was processed and not modified since
        return cache[file]["result"]
    else:
        words = parse(file_path)
        if (len(words) == 0):
            return f'File is empty or could not be found'
        counter = collections.Counter(words)
        result = counter.most_common(n)
        cache[file] = {
            "result": result,
            "mtime": os.path.getmtime(os.path.join("database", file))
        }
        store_cache(cache)
        return result

def parse(file = str):
    """Return list of words from file"""
    if os.path.isfile(file) and os.path.getsize(file) > 0:
        with open(file, "r") as f:
            text = f.read()
            words = re.findall(r"[\w'-]+", text) # find all words in file
            words = [word.lower() for word in words] # lowercase words
            return words
    return ''

def get_cache(cache_file = CACHE_FILE):
    """Return cache object from cache_file or empty object if it doesn't exist."""
    if os.path.isfile(cache_file) and os.path.getsize(cache_file) > 0:
        with open(cache_file, "r") as f:
            return json.load(f)
    return {}

def store_cache(cache, cache_file = CACHE_FILE):
    """Store cache object on cache_file."""
    with open(cache_file, "w+") as f:
        json.dump(cache, f)