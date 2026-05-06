import re

# =====================================
# DETECTION ENGINE
# =====================================

def detect(response, payload):

    findings = []

    text = response.text.lower()

    payload_lower = payload.lower()

    # =================================
    # REFLECTION DETECTION
    # =================================

    if payload_lower in text:

        findings.append("reflection")

    # =================================
    # BASIC XSS DETECTION
    # =================================

    xss_patterns = [
        "<script>alert(1)</script>",
        "onerror=",
        "onload=",
        "<svg",
        "alert(1)"
    ]

    for pattern in xss_patterns:

        if pattern.lower() in text:

            findings.append("xss")

            break

    # =================================
    # SQL ERROR DETECTION
    # =================================

    sql_errors = [

        "sql syntax",

        "mysql_fetch",

        "ora-01756",

        "postgresql",

        "warning: mysql",

        "unclosed quotation mark",

        "quoted string not properly terminated",

        "sqlite error",

        "sqlstate",

        "syntax error"
    ]

    for error in sql_errors:

        if error.lower() in text:

            findings.append("sqli")

            break

    # =================================
    # LFI DETECTION
    # =================================

    lfi_patterns = [
        "root:x:0:0",
        "[boot loader]",
        "/bin/bash",
        "daemon:x"
    ]

    for pattern in lfi_patterns:

        if pattern.lower() in text:

            findings.append("lfi")

            break

    # =================================
    # RFI DETECTION
    # =================================

    if "http://" in text or "https://" in text:

        if payload_lower in text:

            findings.append("rfi")

    return list(set(findings))
