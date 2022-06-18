import asyncio
import time


async def timer(sec, callback, *callback_args, **callback_kwargs):
    await asyncio.sleep(sec)
    callback(*callback_args, **callback_kwargs)


class Timer:
    def __init__(self):
        pass

    def run(self, sec, callback, *callback_args, **callback_kwargs):
        asyncio.run(timer(sec, callback, *callback_args, **callback_kwargs))

a = True
def cb(arg):
    global a
    a = False
    print(arg)


if __name__ == "__main__":
    t = Timer()
    t.run(10, cb, (123,))
    b = 0
    while a:
        print(b)
        b+=1
        time.sleep(0.5)
