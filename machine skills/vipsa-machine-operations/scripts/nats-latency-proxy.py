#!/usr/bin/env python3
"""One-client-compatible local NATS latency bridge for PUDA CLI.

It immediately sends local INFO/PONG while a high-latency Tailscale/DERP
upstream connection is opening, buffers initial CONNECT/SUB/PUB lines, then
forwards them after consuming upstream INFO. Use a different local port per
bridge and stop the process immediately after the bounded PUDA operation.
"""
import argparse, asyncio, json

async def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--remote-host',required=True)
    ap.add_argument('--remote-port',type=int,default=4222)
    ap.add_argument('--local-port',type=int,default=54222)
    ap.add_argument('--upstream-timeout',type=float,default=15)
    a=ap.parse_args()
    fake=("INFO "+json.dumps({"server_id":"local-proxy","server_name":"local-proxy","version":"2.10.0","proto":1,"go":"go1.22","host":"127.0.0.1","port":a.local_port,"max_payload":1048576},separators=(',',':'))+"\r\n").encode()

    async def pipe(src,dst):
        try:
            while data:=await src.read(65536):
                dst.write(data); await dst.drain()
        finally:
            try: dst.close()
            except Exception: pass

    async def handle(r,w):
        w.write(fake); await w.drain()
        task=asyncio.create_task(asyncio.open_connection(a.remote_host,a.remote_port))
        buffered=[]; partial=b''
        while not task.done():
            try: data=await asyncio.wait_for(r.read(65536),.1)
            except asyncio.TimeoutError: continue
            if not data: break
            partial+=data
            while b'\r\n' in partial:
                line,partial=partial.split(b'\r\n',1)
                if line==b'PING':
                    w.write(b'PONG\r\n'); await w.drain()
                else: buffered.append(line+b'\r\n')
        if partial: buffered.append(partial)
        try: rr,rw=await asyncio.wait_for(task,a.upstream_timeout)
        except Exception: w.close(); return
        try: await asyncio.wait_for(rr.readline(),5)
        except Exception: w.close(); rw.close(); return
        for data in buffered: rw.write(data)
        await rw.drain()
        await asyncio.gather(pipe(r,rw),pipe(rr,w),return_exceptions=True)

    server=await asyncio.start_server(handle,'127.0.0.1',a.local_port)
    async with server: await server.serve_forever()

asyncio.run(main())
