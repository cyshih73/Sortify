# Sortify
A python, API based tool to sort the playlist by album release date

## Requirements
- python 3 (3.6, 3.8 Tested)

## Instructions
1. Get your OAuth2 token on [Spotify Developer](https://developer.spotify.com/console/get-track), "OAuth Token" section
  ![spotify API](https://i.imgur.com/sBX2QP4.png)
  > Scopes needed: "playlist-modify-public", "playlist-read-public", "playlist-modify-public", "playlist-read-public"
  ![spotify scopes](https://i.imgur.com/Jp37PHj.png)

2. python main.py -i [Id of target playlist] -u [Your username] -a [OAuth Token]
3. A playlist named [Name of target playlist]_sorted will be in your list of playlists

## Notes
To acquire the playlist Id:
1. Right click the playlist
2. Share -> Copy link to playlist
3. `https://open.spotify.com/playlist/[Id of target playlist]?si=[Doesn't matter]`

## TODOs
1. Auto OAuth
2. Add more sort keys
3. Web service
