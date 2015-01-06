#!/usr/bin/env python
import sys
import json
import asyncio
import atexit
import websockets
from subprocess import call

locked = {}

def switch_led(on):
    call(["xset", "led" if on else "-led" , "named", "Scroll Lock"])


@asyncio.coroutine
def hello(base_url):
    websocket = yield from websockets.connect('ws://{}/changes'.format(base_url))
    while True:
        msg = yield from websocket.recv()
        msg = json.loads(msg)
        locked[msg['name']] = msg['state'] == 'locked'
        occupied = any(locked.values())
        #TODO something like on/flashing can be used to signalize one/two occupied
        switch_led(occupied)

@atexit.register
def switch_off():
    switch_led(False)

if __name__ == "__main__":
    base_url = 'itoilet' if len(sys.argv) == 1 else sys.argv[1]
    asyncio.get_event_loop().run_until_complete(hello(base_url))



