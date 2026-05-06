from urllib.parse import (
    urlparse,
    parse_qs,
    urlencode,
    urlunparse
)

# =====================================
# FUZZ ONE PARAMETER AT A TIME
# =====================================

def inject(url, value):

    fuzzed_urls = []

    parsed = urlparse(url)

    params = parse_qs(parsed.query)

    # fuzz each parameter individually
    for target_param in params.keys():

        new_params = params.copy()

        # replace only one parameter
        new_params[target_param] = value

        encoded = urlencode(
            new_params,
            doseq=True
        )

        fuzzed = urlunparse(
            parsed._replace(query=encoded)
        )

        fuzzed_urls.append(fuzzed)

    return fuzzed_urls

# =====================================
# SINGLE PARAM REPLACEMENT
# =====================================

def inject_per_param(
    url,
    param_name,
    payload
):

    parsed = urlparse(url)

    params = parse_qs(parsed.query)

    if param_name not in params:
        return url

    new_params = params.copy()

    # replace only selected param
    new_params[param_name] = payload

    encoded = urlencode(
        new_params,
        doseq=True
    )

    return urlunparse(
        parsed._replace(query=encoded)
    )
