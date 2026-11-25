"""Exercise the actual HTTP handler over byte streams when loopback is restricted.

No mocked domain service or API responses. This is HTTP protocol integration,
not a socket/TLS deployment test. Also used by browser E2E via a stdio bridge.
"""
import http.client
import io
import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'app'))
from domain import Store
from server import Handler


class Wire:
    def __init__(self, incoming):
        self.incoming = io.BytesIO(incoming)
        self.outgoing = bytearray()

    def makefile(self, mode, *args):
        return self.incoming

    def sendall(self, data):
        self.outgoing.extend(data)


def request(store, method, path, body=b'', headers=None, origin='http://127.0.0.1:8000'):
    h = {'Host': origin.split('://')[1], 'Content-Length': str(len(body)), 'Connection': 'close', **(headers or {})}
    wire = Wire((method + ' ' + path + ' HTTP/1.1\r\n' + ''.join(f'{k}: {v}\r\n' for k, v in h.items()) + '\r\n').encode() + body)
    Handler(wire, ('127.0.0.1', 12345), SimpleNamespace(store=store, origin=origin, secure=False))
    response = http.client.HTTPResponse(Wire(bytes(wire.outgoing)))
    response.begin()
    return response.status, dict(response.getheaders()), response.read()


def main():
    import base64
    store = Store(sys.argv[1])
    for line in sys.stdin:
        try:
            p = json.loads(line)
            status, headers, body = request(store, p['method'], p['path'], base64.b64decode(p.get('body', '')), p.get('headers'))
            print(json.dumps({'status': status, 'headers': headers, 'body': base64.b64encode(body).decode()}), flush=True)
        except Exception as exc:
            print(json.dumps({'error': str(exc)}), flush=True)


if __name__ == '__main__':
    main()
