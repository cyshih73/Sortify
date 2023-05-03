# -*- coding: UTF-8 -*-
import requests
from argparse import ArgumentParser

# Error handling
def error(response):
    print("E: %d - %s" % (response.status_code, response.json()['error']['message']))
    exit()


# Get the target playlist's name and tracks
def get_playlist(token, pl_id):
    header = { 'Content-Type': 'application/json', 'Authorization': token }
    
    # Get the playlist name
    uri = 'https://api.spotify.com/v1/playlists/%s' % pl_id
    field = uri + '?fields=name'
    response = requests.get(field, headers=header)
    if response.status_code != 200: error(response)
    pl_name = response.json()['name']

    # Get the tracks
    uri, tracks = 'https://api.spotify.com/v1/playlists/%s/tracks' % pl_id, []
    # Only 100 data can be retrieved at once
    count, total = 0, 1000
    while count < total:
        field = uri+'?fields=total,items(track(name,id,album(release_date)))&limit=50&offset=%d' % count
        response = requests.get(field, headers=header)
        if response.status_code != 200: error(response)
        total = response.json()['total']
        tracks = tracks + response.json()['items']
        count += 50

    print("Got %d tracks in playlist \"%s.\"" % (total, pl_name))
    return pl_name, tracks

# Create the "_sorted" playlist
def create_playlist(token, username, pl_name):
    uri = 'https://api.spotify.com/v1/users/%s/playlists' % username
    header = { 'Content-Type': 'application/json', 'Authorization': token }
    payload = { 'name': pl_name+'_sorted' }

    response = requests.post(uri, json=payload, headers=header)
    if response.status_code != 201: error(response)
    print(response.json()['name'] + ' Created.')
    return response.json()['id']

# Put the tracks into new playlists
def put_into_pl(token, pl_id, tracks):
    uri = 'https://api.spotify.com/v1/playlists/%s/tracks' % pl_id
    header = { 'Content-Type': 'application/json', 'Authorization': token }
    payload = { 'uris': tracks }

    response = requests.post(uri, json=payload, headers=header)
    if response.status_code != 201: error(response)
    print(response, response.text)
    return response

# Sortkey
def json_key(json):
    try: return json['track']['album']['release_date']
    except: return 0

# Split the tracks array to chunks
def chunks(l, n):
    for i in range(0, len(l), n): yield l[i:i+n]

def main(args):
    token = 'Bearer ' + args.access_token

    pl_name, tracks = get_playlist(token, args.pl_id)
    tracks.sort(key=json_key, reverse=True)
    tracks_uris = []
    for i in range(len(tracks)):
        tracks_uris.append('spotify:track:' + tracks[i]['track']['id'])
        print(tracks[i]['track']['album']['release_date'], tracks[i]['track']['name'])

    npl_id = create_playlist(token, args.username, pl_name)

    # Only 100 rows can be retrieved at once
    tracks_uris = list(chunks(tracks_uris, 80))
    for tracks_uri in tracks_uris:
        put_into_pl(token, npl_id ,tracks_uri)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-u", "--user", type=str, help="UserName", required=True, dest="username")
    parser.add_argument("-i", "--pid", type=str, help="Playlist Id", required=True, dest="pl_id")
    parser.add_argument("-a", "--access_token", type=str, help="access_token", required=True, dest="access_token")
    args = parser.parse_args()
    main(args)
