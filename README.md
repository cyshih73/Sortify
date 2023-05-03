# Sortify
A python, API based tool to sort the playlist by album release date

## Requirements
- python 3 (3.6, 3.8, 3.9 Tested)

## Instructions
1. Get your OAuth2 token
    1. [Create an app](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#create-an-app)
        * Enter `http://localhost` as Redirect URIs under Basic Information
        * Copy the `client_id` and `client_secret` here
    1. Run OAuth2 by change the `client_id` to the one copied in the last step and paste the uri in the browser. This will bring you to `http://localhost/?code=[authorization code]`. Copy the `authorization code` part.
        ```
        https://accounts.spotify.com/authorize?client_id=[client_id]&redirect_uri=http://localhost&response_type=code&scope=playlist-read-private playlist-modify-public playlist-modify-private
        ```
    1. Get the Access token with `curl`. Encode `[client_id]:[cliend_secret]` with Base64. I used [this web tool](https://www.base64encode.org)
        ```
        curl -X POST "https://accounts.spotify.com/api/token" \
             -H "Content-Type: application/x-www-form-urlencoded" \
             -H "Authorization: Basic [Base64 encoded client_id:cliend_secret]" \
             -d "grant_type=authorization_code&redirect_uri=http://localhost&code=[the authorization code]"
        ```
    1. Voila! `access_token` is the token you want.
2. python main.py -i [PlaylistId] -u [UserId] -a [access_token]
    * UserId: [Spotify user ID](https://developer.spotify.com/documentation/web-api/concepts/spotify-uris-ids)
    * PlaylistId: 
        1. Right click the playlist
        1. Share -> Copy link to playlist
        1. `https://open.spotify.com/playlist/[Id of target playlist]?si=[Doesn't matter]`
3. A playlist named [Name of target playlist]_sorted will be in your list of playlists

## TODOs
1. Auto OAuth
2. Add more sort keys
3. Web service
