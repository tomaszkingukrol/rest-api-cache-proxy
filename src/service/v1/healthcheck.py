import asyncio
from tabulate import tabulate


async def get_healthcheck():
    try:
        ct = list(asyncio.all_tasks(loop=asyncio.get_event_loop()))
    except:
        data = {
            'status: ': 'bad'
        }        
    else:
        data = {
            'status: ': 'ok',
            'current tasks: ': str(len(ct)-3)
        }
    finally:
        return tabulate([(k,v) for k, v in data.items()], tablefmt='html')