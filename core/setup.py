import subprocess
import shutil
import sys
import os

from core.logger import info

# =====================================
# GO TOOLS
# =====================================

TOOLS = {
    "waybackurls": "go install github.com/tomnomnom/waybackurls@latest",
    "gau": "go install github.com/lc/gau/v2/cmd/gau@latest"
}

# =====================================
# PYTHON PACKAGES
# =====================================

PYTHON_PACKAGES = [
    "requests",
    "httpx",
    "beautifulsoup4"
]

# =====================================
# SETUP CACHE FILE
# =====================================

SETUP_FILE = ".paramine_setup"

# =====================================
# TOOL EXISTS
# =====================================

def tool_exists(tool):

    # NORMAL PATH
    if shutil.which(tool):
        return True

    # GOPATH/BIN FALLBACK
    try:

        gopath = subprocess.check_output(
            ["go", "env", "GOPATH"],
            text=True
        ).strip()

        gobin = os.path.join(
            gopath,
            "bin",
            tool
        )

        if os.path.exists(gobin):

            # AUTO ADD TO PATH
            os.environ["PATH"] += (
                os.pathsep
                + os.path.join(gopath, "bin")
            )

            return True

    except:
        pass

    return False

# =====================================
# SETUP DONE
# =====================================

def setup_done():

    return os.path.exists(
        SETUP_FILE
    )

# =====================================
# MARK DONE
# =====================================

def mark_setup_done():

    with open(SETUP_FILE, "w") as f:
        f.write("done")

# =====================================
# ENSURE GO
# =====================================

def ensure_go():

    if not tool_exists("go"):

        print(
            "\n[ERROR] Go is not installed\n"
            "Download Go from:\n"
            "https://go.dev/dl/\n"
        )

        sys.exit()

# =====================================
# ENSURE GO PATH
# =====================================

def ensure_go_path():

    try:

        gopath = subprocess.check_output(
            ["go", "env", "GOPATH"],
            text=True
        ).strip()

        gobin = os.path.join(
            gopath,
            "bin"
        )

        # ADD RUNTIME PATH
        if gobin not in os.environ["PATH"]:

            os.environ["PATH"] += (
                os.pathsep + gobin
            )

    except:
        pass

# =====================================
# INSTALL PYTHON PACKAGE
# =====================================

def install_python_package(package):

    try:

        info(
            f"[SETUP] Installing {package}"
        )

        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                package
            ],
            check=False
        )

    except Exception as e:

        print(f"[PIP ERROR] {e}")

# =====================================
# INSTALL GO TOOL
# =====================================

def install_go_tool(name, command):

    try:

        info(
            f"[SETUP] Installing {name}"
        )

        subprocess.run(
            command,
            shell=True,
            check=False,
            env=os.environ
        )

    except Exception as e:

        print(f"[GO INSTALL ERROR] {e}")

# =====================================
# FIX PLAYWRIGHT
# =====================================

def fix_playwright():

    info(
        "[SETUP] Fixing Playwright"
    )

    try:

        # REMOVE SYSTEM PLAYWRIGHT
        subprocess.run(
            [
                "sudo",
                "apt",
                "remove",
                "-y",
                "python3-playwright"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

    except:
        pass

    try:

        # REMOVE PIP PLAYWRIGHT
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "uninstall",
                "-y",
                "playwright"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

    except:
        pass

    # INSTALL CLEAN PLAYWRIGHT
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "playwright"
        ],
        check=False
    )

    # INSTALL CHROMIUM
    subprocess.run(
        [
            "playwright",
            "install",
            "chromium"
        ],
        check=False
    )

# =====================================
# ENSURE PYTHON PACKAGES
# =====================================

def ensure_python_packages():

    for package in PYTHON_PACKAGES:

        try:

            __import__(package)

        except:

            install_python_package(
                package
            )

# =====================================
# ENSURE GO TOOLS
# =====================================

def ensure_go_tools():

    for tool, command in TOOLS.items():

        if not tool_exists(tool):

            install_go_tool(
                tool,
                command
            )

# =====================================
# TEST PLAYWRIGHT
# =====================================

def playwright_ok():

    try:

        from playwright.async_api import (
            async_playwright
        )

        return True

    except:
        return False

# =====================================
# SETUP ENVIRONMENT
# =====================================

def setup_environment():

    # ---------------------------------
    # GO
    # ---------------------------------

    ensure_go()

    ensure_go_path()

    # ---------------------------------
    # ALREADY SETUP
    # ---------------------------------

    if setup_done():

        info(
            "[SETUP] Environment already ready"
        )

        # STILL VERIFY PLAYWRIGHT
        if not playwright_ok():

            fix_playwright()

        return

    info("[SETUP] Checking environment")

    # ---------------------------------
    # PYTHON PACKAGES
    # ---------------------------------

    ensure_python_packages()

    # ---------------------------------
    # GO TOOLS
    # ---------------------------------

    ensure_go_tools()

    # ---------------------------------
    # PLAYWRIGHT
    # ---------------------------------

    fix_playwright()

    # ---------------------------------
    # DONE
    # ---------------------------------

    mark_setup_done()

    info("[SETUP] Environment ready")
