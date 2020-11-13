import os
import http.client
from flask import abort
import json


COFFEE_SERVER_CLIENT_ID = os.getenv("COFFEE_SERVER_CLIENT_ID")
COFFEE_SERVER_CLIENT_SECRET = os.getenv("COFFEE_SERVER_CLIENT_SECRET")
MANAGEMENT_API_AUDIENCE = os.getenv("MANAGEMENT_API_AUDIENCE")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")


def get_access_token():
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = json.dumps({
        "client_id": COFFEE_SERVER_CLIENT_ID,
        "client_secret": COFFEE_SERVER_CLIENT_SECRET,
        "audience": MANAGEMENT_API_AUDIENCE,
        "grant_type": "client_credentials"
    })
    headers = {'content-type': "application/json"}

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()
    if res.code != 200:
        return ''
    return json.loads(data.decode("utf-8"))['access_token']


def get_registered_users():
    access_token = get_access_token()
    headers = {'Authorization': f"Bearer {access_token}"}
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)

    conn.request("GET", "/api/v2/users", headers=headers)

    res = conn.getresponse()
    data = res.read()

    users = json.loads(data.decode("utf-8"))

    return users


def get_barista_id():
    access_token = get_access_token()
    headers = {'Authorization': f"Bearer {access_token}"}
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)

    conn.request("GET", "/api/v2/roles?name_filter=Barista", headers=headers)

    res = conn.getresponse()
    if res.code != 200:
        return None

    data = res.read()

    roles = json.loads(data.decode("utf-8"))

    if len(roles) < 1:
        return None

    barista_id = [0]["id"]
    return barista_id


def get_user_roles(user_id):
    access_token = get_access_token()
    headers = {'Authorization': f"Bearer {access_token}"}
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    conn.request("GET", f"/api/v2/users/{user_id}/roles", headers=headers)
    res = conn.getresponse()
    if res.code == 401:
        abort(422)

    if res.code == 404:
        abort(404)

    if res.code != 200:
        abort(422)

    res_data = res.read()
    roles = json.loads(res_data.decode("utf-8"))

    return roles


def roles_contain(roles, role_name):
    return any(
        x['name'].lower() == role_name.lower() for x in roles)


def add_role_to_user(user_id, role_id):
    access_token = get_access_token()
    headers = {
        'Authorization': f"Bearer {access_token}",
        'content-type': "application/json"}
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = json.dumps({
        "roles": [
            role_id
        ]
    })
    conn.request("POST", f"/api/v2/users/{user_id}/roles", payload, headers)
    return conn.getresponse()


def remove_role_from_user(user_id, role_id):
    access_token = get_access_token()
    headers = {}
    headers = {
        'Authorization': f"Bearer {access_token}",
        'content-type': "application/json"}
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = json.dumps({
        "roles": [
            role_id
        ]
    })
    conn.request(
        "DELETE", f"/api/v2/users/{user_id}/roles", payload, headers)
    return conn.getresponse()
