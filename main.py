# -*- coding: UTF-8 -*-
# Get your access token on:
# https://developer.spotify.com/console/get-track
import json
import requests
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from argparse import ArgumentParser

def get_playlists(token):
    uri = 'https://api.spotify.com/v1/me/playlists'
    header = { 'Content-Type': 'application/json', 'Authorization': token }
    response = requests.get(uri, headers=header)
    print("Got %d lists." % len(response.json()['items']))
    return response.json()['items']

def create_playlist(token, username, pl_name):
    uri = 'https://api.spotify.com/v1/users/%s/playlists' % username
    header = { 'Content-Type': 'application/json', 'Authorization': token }
    payload = { 'name': pl_name+'_sorted' }

    response = requests.post(uri, json=payload, headers=header)
    print(response.json()['name'] + ' Created.')
    return response.json()['id']

def get_playlist(token, list_id):
    uri = 'https://api.spotify.com/v1/playlists/%s/tracks' % list_id
    header = { 'Content-Type': 'application/json', 'Authorization': token }
    tracks = []
    count, total = 0, 1000
    while count < total:
        field = uri+'?fields=total,items(track(name,id,album(release_date)))&limit=100&offset=%d' % count
        response = requests.get(field, headers=header)
        total = response.json()['total']
        tracks = tracks + response.json()['items']
        count += 100

    print("Got %d tracks in %s." % (total, list_id))
    return tracks

def put_into_pl(token, list_id, tracks):
    uri = 'https://api.spotify.com/v1/playlists/%s/tracks' % list_id
    header = { 'Content-Type': 'application/json', 'Authorization': token }
    payload = { 'uris': tracks }

    response = requests.post(uri, json=payload, headers=header)
    print(response, response.text)
    return response

def json_key(json):
    try: return json['track']['album']['release_date']
    except: return 0

def chunks(l, n):
    for i in range(0, len(l), n): yield l[i:i+n]

def main(args):
    if args.access_token: token = args.access_token

    #=====================================================================
    # Working on playlists
    token = 'Bearer ' + token
    pls = get_playlists(token)

    npl_id, pl_id, not_created = '', '', True
    for pl in pls:
        if pl['name'] == args.pl_name: pl_id = pl['id']
        elif (pl['name'] == args.pl_name+'_sorted'): 
            not_created = False
            npl_id = pl['id']

    if pl_id and not_created: 
        npl_id = create_playlist(token, args.username, args.pl_name)
    elif pl_id == '': print("Playlist not found.")

    tracks = get_playlist(token, pl_id)

    tracks.sort(key=json_key, reverse=True)
    tracks_uris = []
    for i in range(len(tracks)):
        tracks_uris.append('spotify:track:' + tracks[i]['track']['id'])
        print(tracks[i]['track']['album']['release_date'], tracks[i]['track']['name'])

    tracks_uris = list(chunks(tracks_uris, 80))
    for tracks_uri in tracks_uris:
        put_into_pl(token, npl_id ,tracks_uri)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-u", "--user", type=str, help="UserName", required=True, dest="username")
    parser.add_argument("-l", "--list", type=str, help="playlist Name", required=True, dest="pl_name")
    parser.add_argument("-a", "--access_token", type=str, help="access_token", required=True, dest="access_token")
    args = parser.parse_args()
    main(args)
