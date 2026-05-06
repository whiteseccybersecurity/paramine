import subprocess

from core.logger import info

def run_waybackurls(domain):

    urls = set()

    try:

        info(
            f"[WAYBACKURLS] Extracting URLs from {domain}"
        )

        cmd = f"echo {domain} | waybackurls"

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True
        )

        for line in result.stdout.splitlines():

            line = line.strip()

            if line:

                urls.add(line)

                info(f"[URL] {line}")

    except Exception as e:
        print(f"[WAYBACKURLS ERROR] {e}")

    return sorted(list(urls))
