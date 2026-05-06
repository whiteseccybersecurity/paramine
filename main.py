# =====================================
# PARAMINE - FIXED main.py
# =====================================

import asyncio
import os
import sys
import httpx

from urllib.parse import (
    urlparse,
    parse_qs,
    urlencode,
    urlunparse
)

from core.logger import (
    info,
    vuln,
    set_verbose
)

from core.setup import setup_environment

from core.cache import (
    load_cache,
    save_cache,
    mark_tested,
    is_tested
)

from core.output import (
    dedupe_urls,
    unique_vulns
)

from core.providers import (
    run_waybackurls
)

from core.filter import (
    filter_params
)

from core.alive import (
    check_alive
)

from core.injector import (
    inject
)

from core.mutator import (
    mutate_payload
)

from core.detector import (
    detect
)

from core.payloads import (
    load_payloads
)

from core.smart_selector import (
    get_payloads_for_param
)

from core.screenshot import (
    take_screenshot,
    init_screenshot_engine
)

# =====================================
# GLOBAL WORKSPACE
# =====================================

WORKSPACE = ""

# =====================================
# SAFE INPUT
# =====================================

def safe_input(message):

    try:
        return input(message)

    except KeyboardInterrupt:

        print("\n\n[INFO] Interrupted by user")

        sys.exit(0)

# =====================================
# WORKSPACE
# =====================================

def choose_workspace():

    global WORKSPACE

    path = safe_input(
        "\nEnter workspace folder "
        "(leave empty for current directory): "
    ).strip()

    path = path.replace('"', "")

    if not path:
        path = os.getcwd()

    if not os.path.exists(path):

        try:
            os.makedirs(path)

        except:

            print("[ERROR] Cannot create workspace")

            sys.exit(1)

    WORKSPACE = path

    print(f"\n[WORKSPACE] {WORKSPACE}\n")

# =====================================
# TARGET PATH
# =====================================

def target_path(domain):

    return os.path.join(
        WORKSPACE,
        domain
    )

# =====================================
# BANNER
# =====================================

def banner():

    print("""

PARAMINE FRAMEWORK

1. Recon
2. FUZZ
3. Manual Scan
4. Smart Scan
5. Help

""")

# =====================================
# HELP
# =====================================

def help_menu():

    print("""

Recon
------
Extract archived URLs
Filter parameters
Check alive URLs

FUZZ
----
Replace parameter values

Manual Scan
-----------
Use custom payload files

Smart Scan
-----------
Automatic payload selection

Features
--------
- Workspace support
- Drag & drop URL files
- Resume support
- Screenshot support
- Smart payload mutation
- Multi-parameter fuzzing
- Graceful interrupt handling

""")

# =====================================
# FILE LOADER
# =====================================

def choose_url_file():

    path = safe_input(
        "\nDrag & drop URL file: "
    ).strip()

    path = path.replace('"', "")

    if not os.path.exists(path):

        print("[ERROR] File not found")

        return []

    with open(path) as f:

        urls = [
            x.strip()
            for x in f
            if x.strip()
        ]

    print(
        f"\n[INFO] Loaded {len(urls)} URLs\n"
    )

    return urls

# =====================================
# TARGETS
# =====================================

def get_targets():

    choice = safe_input(
        "1. Single Domain  2. List: "
    )

    # SINGLE
    if choice == "1":

        domain = safe_input(
            "Enter domain: "
        ).strip()

        if not domain:

            print("[ERROR] Empty domain")

            return []

        return [domain]

    # LIST
    elif choice == "2":

        file = safe_input(
            "Enter file path: "
        )

        file = file.replace('"', "")

        if not os.path.exists(file):

            print("[ERROR] File not found")

            return []

        with open(file) as f:

            domains = [
                x.strip()
                for x in f
                if x.strip()
            ]

        if not domains:

            print("[ERROR] Empty domain list")

            return []

        return domains

    else:

        print("[ERROR] Invalid option")

        return []

# =====================================
# RECON
# =====================================

async def recon(
    domain,
    threads,
    resume
):

    domain_dir = target_path(domain)

    os.makedirs(
        domain_dir,
        exist_ok=True
    )

    cache = load_cache(domain_dir)

    # =================================
    # WAYBACK
    # =================================

    if resume and cache["wayback_done"]:

        with open(
            os.path.join(
                domain_dir,
                "all_wayback.txt"
            )
        ) as f:

            urls = [
                x.strip()
                for x in f
            ]

    else:

        urls = run_waybackurls(domain)

        with open(
            os.path.join(
                domain_dir,
                "all_wayback.txt"
            ),
            "w"
        ) as f:

            f.write("\n".join(urls))

        cache["wayback_done"] = True

    # =================================
    # FILTER PARAMETERS
    # =================================

    filtered = filter_params(urls)

    param_urls = filtered["param_urls"]

    unique_params = filtered["unique_params"]

    patterns = filtered["patterns"]

    with open(
        os.path.join(
            domain_dir,
            "all_params.txt"
        ),
        "w"
    ) as f:

        f.write("\n".join(param_urls))

    with open(
        os.path.join(
            domain_dir,
            "unique_params.txt"
        ),
        "w"
    ) as f:

        f.write("\n".join(unique_params))

    with open(
        os.path.join(
            domain_dir,
            "param_patterns.txt"
        ),
        "w"
    ) as f:

        f.write("\n".join(patterns))

    info(
        f"[FILTER] Parameter URLs: {len(param_urls)}"
    )

    info(
        f"[FILTER] Unique Parameters: {len(unique_params)}"
    )

    # =================================
    # ALIVE CHECK
    # =================================

    if resume and cache["alive_done"]:

        with open(
            os.path.join(
                domain_dir,
                "alive_params.txt"
            )
        ) as f:

            alive = [
                x.strip()
                for x in f
            ]

    else:

        info("[ALIVE] Checking URLs")

        alive = dedupe_urls(
            await check_alive(
                param_urls,
                threads
            )
        )

        with open(
            os.path.join(
                domain_dir,
                "alive_params.txt"
            ),
            "w"
        ) as f:

            f.write("\n".join(alive))

        cache["alive_done"] = True

    save_cache(
        domain_dir,
        cache
    )

    info(
        f"[ALIVE] Alive URLs: {len(alive)}"
    )

# =====================================
# FUZZ
# =====================================

def fuzz(urls, domain):

    value = safe_input(
        "Value (default FUZZ): "
    ) or "FUZZ"

    dedupe = safe_input(
        "Remove duplicate URLs? (y/n): "
    ).lower() == "y"

    fuzzed = []

    for url in urls:

        fuzzed.extend(
            inject(url, value)
        )

    original_count = len(fuzzed)

    if dedupe:

        fuzzed = dedupe_urls(fuzzed)

    os.makedirs(
        target_path(domain),
        exist_ok=True
    )

    output = os.path.join(
        target_path(domain),
        "fuzzed.txt"
    )

    with open(output, "w") as f:

        f.write("\n".join(fuzzed))

    print(
        f"\n[FUZZ] Original: {original_count}"
    )

    print(
        f"[FUZZ] Final: {len(fuzzed)}"
    )

    print(
        f"[FUZZ] Saved: {output}\n"
    )

# =====================================
# MANUAL SCAN
# =====================================

async def manual_scan(
    urls,
    domain,
    screenshot,
    resume
):

    os.makedirs(
        target_path(domain),
        exist_ok=True
    )

    cache = load_cache(
        target_path(domain)
    )

    use_file = safe_input(
        "Use payload file? (y/n): "
    ).lower() == "y"

    if use_file:

        file = safe_input(
            "Payload file path: "
        )

        file = file.replace('"', "")

        payloads = load_payloads(file)

    else:

        payloads = [
            "<script>alert(1)</script>"
        ]

    results = []

    shot_dir = os.path.join(
        target_path(domain),
        "screenshots"
    )

    if screenshot:

        os.makedirs(
            shot_dir,
            exist_ok=True
        )

    async with httpx.AsyncClient(
        timeout=10,
        follow_redirects=True,
        verify=False
    ) as client:

        try:

            for payload in payloads:

                for mutation in mutate_payload(payload):

                    for i, url in enumerate(urls):

                        if resume and is_tested(
                            cache,
                            url,
                            mutation
                        ):
                            continue

                        fuzzed_urls = inject(
                            url,
                            mutation
                        )

                        for test_url in fuzzed_urls:

                            info(
                                f"[SCAN] {test_url}"
                            )

                            try:

                                r = await client.get(
                                    test_url
                                )

                                mark_tested(
                                    cache,
                                    url,
                                    mutation
                                )

                                findings = detect(
                                    r,
                                    mutation
                                )

                                # =================================
                                # REFLECTION OR VULN
                                # =================================

                                if (
                                    findings
                                    or mutation.lower()
                                    in r.text.lower()
                                ):

                                    result = (
                                        f"[{','.join(findings).upper()}] "
                                        f"{test_url}"
                                    )

                                    results.append(result)

                                    vuln(
                                        f"[VULN] {result}"
                                    )

                                    # =================================
                                    # SCREENSHOT
                                    # =================================

                                    if screenshot:

                                        path = os.path.join(
                                            shot_dir,
                                            f"{hash(test_url)}.png"
                                        )

                                        info(
                                            f"[SCREENSHOT] {path}"
                                        )

                                        await take_screenshot(
                                            test_url,
                                            path
                                        )

                            except:
                                pass

        except KeyboardInterrupt:

            print("\n[INFO] Scan stopped")

            save_cache(
                target_path(domain),
                cache
            )

            return

    results = unique_vulns(results)

    save_cache(
        target_path(domain),
        cache
    )

    with open(
        os.path.join(
            target_path(domain),
            "vuln.txt"
        ),
        "a"
    ) as f:

        f.write(
            "\n".join(results) + "\n"
        )

# =====================================
# SMART SCAN
# =====================================

async def smart_scan(
    urls,
    domain,
    screenshot,
    resume
):

    os.makedirs(
        target_path(domain),
        exist_ok=True
    )

    cache = load_cache(
        target_path(domain)
    )

    results = []

    shot_dir = os.path.join(
        target_path(domain),
        "screenshots"
    )

    if screenshot:

        os.makedirs(
            shot_dir,
            exist_ok=True
        )

    async with httpx.AsyncClient(
        timeout=10,
        follow_redirects=True,
        verify=False
    ) as client:

        try:

            for url in urls:

                parsed = urlparse(url)

                params = parse_qs(
                    parsed.query
                )

                for param_name in params.keys():

                    info(
                        f"\n[PARAM] Testing: {param_name}"
                    )

                    payloads = (
                        get_payloads_for_param(
                            param_name
                        )
                    )

                    for payload in payloads:

                        for mutation in mutate_payload(payload):

                            if resume and is_tested(
                                cache,
                                url,
                                f"{param_name}:{mutation}"
                            ):
                                continue

                            new_params = params.copy()

                            new_params[param_name] = mutation

                            encoded = urlencode(
                                new_params,
                                doseq=True
                            )

                            test_url = urlunparse(
                                parsed._replace(
                                    query=encoded
                                )
                            )

                            info(
                                f"[SCAN] {test_url}"
                            )

                            try:

                                r = await client.get(
                                    test_url
                                )

                                mark_tested(
                                    cache,
                                    url,
                                    f"{param_name}:{mutation}"
                                )

                                findings = detect(
                                    r,
                                    mutation
                                )

                                # =================================
                                # REFLECTION OR VULN
                                # =================================

                                if (
                                    findings
                                    or mutation.lower()
                                    in r.text.lower()
                                ):

                                    result = (
                                        f"[{','.join(findings).upper()}] "
                                        f"{param_name} "
                                        f"→ {test_url}"
                                    )

                                    results.append(result)

                                    vuln(
                                        f"[VULN] {result}"
                                    )

                                    # =================================
                                    # SCREENSHOT
                                    # =================================

                                    if screenshot:

                                        path = os.path.join(
                                            shot_dir,
                                            f"{hash(test_url)}.png"
                                        )

                                        info(
                                            f"[SCREENSHOT] {path}"
                                        )

                                        await take_screenshot(
                                            test_url,
                                            path
                                        )

                            except:
                                pass

        except KeyboardInterrupt:

            print("\n[INFO] Scan stopped")

            save_cache(
                target_path(domain),
                cache
            )

            return

    results = unique_vulns(results)

    save_cache(
        target_path(domain),
        cache
    )

    with open(
        os.path.join(
            target_path(domain),
            "vuln.txt"
        ),
        "a"
    ) as f:

        f.write(
            "\n".join(results) + "\n"
        )

# =====================================
# MAIN
# =====================================

async def main():

    setup_environment()

    # =================================
    # AUTO FIX SCREENSHOT ENGINE
    # =================================

    await init_screenshot_engine()

    choose_workspace()

    banner()

    choice = safe_input("Select: ")

    if choice == "5":

        help_menu()

        return

    quiet = safe_input(
        "Quiet mode? (y/n): "
    ).lower() == "y"

    if quiet:
        set_verbose(False)

    resume = safe_input(
        "Resume previous scan if exists? (y/n): "
    ).lower() == "y"

    # =================================
    # RECON
    # =================================

    if choice == "1":

        targets = get_targets()

        if not targets:
            return

        threads = int(
            safe_input(
                "Threads (20): "
            ) or 20
        )

        for domain in targets:

            await recon(
                domain,
                threads,
                resume
            )

    # =================================
    # FUZZ / SCAN
    # =================================

    elif choice in ["2", "3", "4"]:

        urls = choose_url_file()

        if not urls:
            return

        domain = safe_input(
            "\nProject name: "
        ).strip()

        if not domain:
            domain = "project"

        # FUZZ
        if choice == "2":

            fuzz(
                urls,
                domain
            )

        # MANUAL
        elif choice == "3":

            screenshot = safe_input(
                "Enable screenshots? (y/n): "
            ).lower() == "y"

            await manual_scan(
                urls,
                domain,
                screenshot,
                resume
            )

        # SMART
        elif choice == "4":

            screenshot = safe_input(
                "Enable screenshots? (y/n): "
            ).lower() == "y"

            await smart_scan(
                urls,
                domain,
                screenshot,
                resume
            )

# =====================================
# START
# =====================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        print("\n\n[INFO] Interrupted by user")

        sys.exit(0)

    except Exception as e:

        print(f"\n[ERROR] {e}")

        sys.exit(1)
