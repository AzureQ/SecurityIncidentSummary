import asyncio
import aiohttp
import time
from flask import current_app


async def fetch_incidents_async(base_url, incident_types):
    async with aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(current_app.config.get('ELEVATE_USERNAME'),
                                   current_app.config.get('ELEVATE_PASSWORD')),
            connector=aiohttp.TCPConnector(limit=0)) as session:
        return await fetch_all(session, urls=[f'{base_url}/{incident_type}' for incident_type in incident_types])


async def fetch_all(session, urls):
    return await asyncio.gather(*[asyncio.create_task(fetch(session, url)) for url in urls])


async def fetch(session, url):
    start_time = time.time()
    async with session.get(url) as response:
        if response.status != 200:
            response.raise_for_status()
        data = await response.json()
        print("Fetching", url, "took %s seconds" % (time.time() - start_time))
        return data
