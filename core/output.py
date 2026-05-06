import hashlib

def dedupe_urls(urls):
    return list(dict.fromkeys(urls))

def unique_vulns(results):

    seen = set()

    clean = []

    for result in results:

        key = hashlib.md5(
            result.encode()
        ).hexdigest()

        if key not in seen:

            seen.add(key)

            clean.append(result)

    return clean