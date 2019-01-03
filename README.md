# spotify_sort
A python, API based tool to sort the playlist by album release date

## Requirements
python    3.6
spotipy   1.4.4 (pip3 install spotipy)

## Instructions
1. Get your OAuth2 token on [SpotifyAPI](https://developer.spotify.com/console/get-track), "OAuth Token" section
> Before the author confirm which scopes are needed, check all the scopes xD
2. python main.py -l [Name of target playlist] -u [Your username] -a [OAuth Token]
3. A playlist named [Name of target playlist]_sorted will be in your list of playlists

## Notes
1. The playlist need to be **privated**
2. If the list name contains spaces, add quotation marks while running instruction 2
  - e.g. Get HYPED -> "Get HYPED"

## TODO
1. Confirm which scopes are needed
2. Auto OAuth
