import asyncio
import httpx

from core.logger import info

async def check_alive(urls, threads=20):

    alive = []

    sem = asyncio.Semaphore(threads)

    async with httpx.AsyncClient(
        timeout=15,
        follow_redirects=True,
        verify=False
    ) as client:

        async def worker(url):

            async with sem:

                try:

                    r = await client.get(url)

                    if r.status_code in [
                        200,201,202,204,
                        301,302,307,
                        401,403
                    ]:

                        alive.append(url)

                        info(f"[ALIVE] {url}")

                except:
                    pass

        await asyncio.gather(*[
            worker(u) for u in urls
        ])

    return alive