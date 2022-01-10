import asyncio
import aiohttp
from time import perf_counter
import timeit
import string
import random

sample = 1_000_000
errors = dict()
measure = list()
result = list()


def id_generator(size=2, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


async def test(session, host):
    host, port, request = host, 5000, f'xx-{id_generator()}'
    url = f'http://{host}:{port}/{request}'
    try:
        resp = await session.get(url)
        measure.append(perf_counter())

        if resp.status >=400:
            response = await resp.text()
        else:
            response = await resp.json()
        if resp.status in errors:
            errors[resp.status] += 1
        else:
            errors[resp.status] = 1
    except Exception as ex:
        print(f'... {ex}')


async def main():
    tasks = list()
    conn = aiohttp.TCPConnector(ssl=False)
    headers = {'content-type': 'application/json', 'X-API-Key': '03e64fe9-21bd-42b4-b5ba-b3ebe4453bbe'}
    async with aiohttp.ClientSession(connector=conn, headers=headers) as session:
        for i in range(int(sample/2)):
            await asyncio.sleep(0.001)
            task = asyncio.create_task(test(session, '127.0.0.1'))
            tasks.append(task)
            await asyncio.sleep(0.001)
            task = asyncio.create_task(test(session, '127.0.0.2'))
            tasks.append(task)

        for i in tasks:
            await i


def avg_response_time(data):
    return round(sum(data)/len(data)*1000,2)

if __name__ == '__main__':
    start = perf_counter()
    asyncio.run(main())
    res = perf_counter()-start

    for i in range(len(measure)-1):
        result.append(measure[i+1]-measure[i])
    result.sort(reverse=True)

    print(f'rps:          ',int(sample/res))
    print(f'avg response: ', avg_response_time(result))
    print(f'worst 10%:    ', avg_response_time(result[:int(sample/10)]))
    print(f'worst 1%:     ', avg_response_time(result[:int(sample/100)]))
    print(errors)



