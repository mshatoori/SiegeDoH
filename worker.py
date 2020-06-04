import asyncio
import base64
import itertools
from typing import List

import dns.message
import httpx


class Worker:
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue
        self.tasks: List[asyncio.Task] = []
        self.concurrent_limit = 3

    @staticmethod
    def is_done(task: asyncio.Task):
        if task.done():
            try:
                result = task.result()
                print(result.content)
            except:
                pass
            return True
        return False

    async def run(self):
        doh_server_url = 'dns.google/dns-query'

        headers = {
            "accept": "application/dns-message",
            "content-type": "application/dns-message",
        }

        async with httpx.AsyncClient(headers=headers, http2=True) as client:
            while True:
                while True:
                    self.tasks[:] = itertools.filterfalse(self.is_done, self.tasks)

                    if len(self.tasks) < self.concurrent_limit:
                        break

                    await asyncio.sleep(0.5)

                random_subdomain = await self.queue.get()

                try:
                    query = dns.message.make_query(qname=random_subdomain, rdtype='A')

                    wire = query.to_wire()
                    wire_b64 = base64.urlsafe_b64encode(wire).decode('utf8')

                    final_url = 'https://{}?dns={}'.format(doh_server_url, wire_b64)
                    print('Sending Query: {}'.format(random_subdomain))

                    self.tasks.append(asyncio.create_task(client.get(final_url)))
                finally:
                    self.queue.task_done()
