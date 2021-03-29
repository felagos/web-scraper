import requests
import base64
import pandas

url_base = "https://api.spotify.com/v1"
ep_artist = "/artists/{id}"
id_artist = "6mdiAmATAx73kdxrNrnlao"


def get_access_token():
    client_id = "ce231c4f627c4feeb796ea0bbe6d8727"
    client_secret = "d4975fdfb89b4af891a02b6f8f430a49"
    client_str = f"{client_id}:{client_secret}"
    client_encode = base64.b64encode(client_str.encode("utf-8"))
    client_encode = str(client_encode, "utf-8")

    token_url = "https://accounts.spotify.com/api/token"
    params = {"grant_type": "client_credentials"}
    headers = {"Authorization": f"Basic {client_encode}"}

    response = requests.post(token_url, data=params, headers=headers)

    return response.json()["access_token"]


def request_artist(id, access_token):
    url_artist = url_base + ep_artist.format(id=id)
    headers = {"Authorization": f"Bearer {access_token}"}

    return requests.get(url_artist, headers=headers)


def do_search(query, access_token):
    url_search = url_base + "/search"
    params = {"q": query, "type": "artist"}
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url_search, headers=headers, params=params)

    return response.json()


def get_discography_by_artist(access_token, id_artist):
    url_albums = f"{url_base}/artists/{id_artist}/albums"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url_albums, headers=headers)

    return response.json()["items"][0]


access_token = get_access_token()

artist_detail = request_artist(id_artist, access_token)
search = do_search("Iron+Maiden", access_token)
discography = get_discography_by_artist(access_token, id_artist)

