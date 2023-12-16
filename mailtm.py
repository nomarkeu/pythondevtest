import requests
import time
import json
from flask import Flask, request, copy_current_request_context

MAILTM_HEADERS = {   
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization" : "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3MDI3MzE0NDQsInJvbGVzIjpbIlJPTEVfVVNFUiJdLCJhZGRyZXNzIjoiYW1pdGllNTM0QHdpcmVjb25uZWN0ZWQuY29tIiwiaWQiOiI2NTdkOTUwZTA3ZjhjMGQ2NGMwY2RmYjAiLCJtZXJjdXJlIjp7InN1YnNjcmliZSI6WyIvYWNjb3VudHMvNjU3ZDk1MGUwN2Y4YzBkNjRjMGNkZmIwIl19fQ.7tsPGn57tC8bJocc9JsQ_-dZwHVu2kvfVw3yxls9hLrrFNMwqz826BUmzOi8iiA14nmYNka3NQ9CxCc8CBcxog"
}

class MailTmError(Exception):
    pass

def _make_mailtm_request(request_fn, timeout = 600):
    tstart = time.monotonic()
    error = None
    status_code = None
    while time.monotonic() - tstart < timeout:
        try:
            r = request_fn()
            status_code = r.status_code
            if status_code == 200 or status_code == 201:
                return r.json()
            if status_code != 429:
                break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            error = e
        time.sleep(1.0)
    
    if error is not None:
        raise MailTmError(error) from error
    if status_code is not None:
        raise MailTmError(f"Status code: {status_code}")
    if time.monotonic() - tstart >= timeout:
        raise MailTmError("timeout")
    raise MailTmError("unknown error")

def get_mailtm_domains():
    def _domain_req():
        return requests.get("https://api.mail.tm/domains", headers = MAILTM_HEADERS)
    
    r = _make_mailtm_request(_domain_req)

    return [ x['domain'] for x in r ]

def create_mailtm_account(address, password):
    account = json.dumps({"address": address, "password": password})   
    def _acc_req():
        return requests.post("https://api.mail.tm/accounts", data=account, headers=MAILTM_HEADERS)

    r = _make_mailtm_request(_acc_req)
    assert len(r['id']) > 0


account = json.dumps({"address": "amitie534@wireconnected.com", "password": "mYV~xVE;'\\"})
topic = json.dumps("'/accounts/657d950e07f8c0d64c0cdfb0'")
def _domain_req():
        return requests.get("https://api.mail.tm/messages", headers = MAILTM_HEADERS)
    
#r = _make_mailtm_request(_domain_req)

#message = get_mailtm_domains()

import asyncio
host = "localhost"
port = 18000

async def client(message):
    reader, writer = await asyncio.open_connection(host,port)
    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()


asyncio.run(client("Hello World!"))

