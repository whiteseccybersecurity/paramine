PARAM_PATTERNS = {

    "sqli": [
        "id",
        "uid",
        "user",
        "account"
    ],

    "xss": [
        "q",
        "search",
        "query",
        "name"
    ],

    "lfi": [
        "file",
        "path",
        "page"
    ],

    "redirect": [
        "redirect",
        "url",
        "next"
    ]
}

DEFAULT_PAYLOADS = {

    "sqli": [
        "' OR 1=1--"
    ],

    "xss": [
        "<script>alert(1)</script>"
    ],

    "lfi": [
        "../../../../etc/passwd"
    ],

    "redirect": [
        "https://evil.com"
    ]
}

def detect_param_type(param):

    param = param.lower()

    for vuln, keys in PARAM_PATTERNS.items():

        for k in keys:

            if k in param:
                return vuln

    return "xss"

def get_payloads_for_param(param):

    vuln = detect_param_type(param)

    return DEFAULT_PAYLOADS.get(vuln, [])