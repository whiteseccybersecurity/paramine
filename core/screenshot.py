import os
import subprocess
import asyncio

from playwright.async_api import (
    async_playwright
)

# =====================================
# PLAYWRIGHT STATUS
# =====================================

PLAYWRIGHT_READY = False

# =====================================
# AUTO FIX PLAYWRIGHT
# =====================================

def fix_playwright():

    global PLAYWRIGHT_READY

    try:

        # install browsers silently
        subprocess.run(
            [
                "playwright",
                "install",
                "chromium"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

        PLAYWRIGHT_READY = True

    except:
        PLAYWRIGHT_READY = False

# =====================================
# CHECK PLAYWRIGHT
# =====================================

async def check_browser():

    global PLAYWRIGHT_READY

    try:

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True
            )

            await browser.close()

        PLAYWRIGHT_READY = True

    except:

        PLAYWRIGHT_READY = False

# =====================================
# INIT
# =====================================

async def init_screenshot_engine():

    await check_browser()

    if not PLAYWRIGHT_READY:

        print(
            "\n[SCREENSHOT] "
            "Fixing Playwright environment...\n"
        )

        fix_playwright()

        await check_browser()

        if PLAYWRIGHT_READY:

            print(
                "[SCREENSHOT] Engine ready\n"
            )

        else:

            print(
                "[SCREENSHOT] Disabled "
                "(browser install failed)\n"
            )

# =====================================
# SCREENSHOT
# =====================================

async def take_screenshot(
    url,
    path
):

    global PLAYWRIGHT_READY

    # skip if broken
    if not PLAYWRIGHT_READY:
        return False

    try:

        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ]
            )

            page = await browser.new_page()

            await page.goto(
                url,
                timeout=15000,
                wait_until="domcontentloaded"
            )

            await asyncio.sleep(2)

            os.makedirs(
                os.path.dirname(path),
                exist_ok=True
            )

            await page.screenshot(
                path=path,
                full_page=True
            )

            await browser.close()

            return True

    except Exception as e:

        print(
            f"[SCREENSHOT ERROR] {e}"
        )

        return False
