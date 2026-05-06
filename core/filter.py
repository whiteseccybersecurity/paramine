from urllib.parse import (
    urlparse,
    parse_qs
)

def filter_params(urls):

    param_urls = []

    unique_params = set()

    patterns = set()

    for url in urls:

        try:

            parsed = urlparse(url)

            if parsed.query and "=" in parsed.query:

                param_urls.append(url)

                qs = parse_qs(parsed.query)

                for param in qs.keys():

                    unique_params.add(param)

                    base = (
                        f"{parsed.scheme}://"
                        f"{parsed.netloc}"
                        f"{parsed.path}"
                    )

                    patterns.add(
                        f"{param}={base}?{param}="
                    )

        except:
            pass

    return {
        "param_urls": list(set(param_urls)),
        "unique_params": sorted(unique_params),
        "patterns": sorted(patterns)
    }
