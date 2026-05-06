import json
import os

def cache_path(domain):

    return os.path.join(
        domain,
        ".cache.json"
    )

def load_cache(domain):

    path = cache_path(domain)

    if os.path.exists(path):

        with open(path) as f:
            return json.load(f)

    return {
        "wayback_done": False,
        "alive_done": False,
        "tested": []
    }

def save_cache(domain, data):

    os.makedirs(domain, exist_ok=True)

    with open(cache_path(domain), "w") as f:
        json.dump(data, f, indent=4)

def mark_tested(cache, url, payload):

    key = f"{url}|{payload}"

    if key not in cache["tested"]:
        cache["tested"].append(key)

def is_tested(cache, url, payload):

    return f"{url}|{payload}" in cache["tested"]
