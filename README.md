![Zoom2youtube slack notifications](http://i.imgur.com/2nxeNBG.png)

# Features

- Automatically download a new Zoom video
- Upload the video to YouTube (privacy settings: unlisted)
- Drop a link to the YouTube video into a Slack channel
- Filter settings: will not upload videos under 15 minutes long to prevent uploads of accidental recordings


Quick Start Guide
=========




Step 1 - set up Zoom
----------------------

You need to create a `.env` file in the root directory of the project, specifying the keys listed below:

    ZOOM_KEY
    ZOOM_SECRET
    ZOOM_HOST_ID
    ZOOM_EMAIL
    ZOOM_PASSWORD

To get the keys, follow these steps:
1. Follow the link: https://api.zoom.us/developer/api/credential
2. Enable the API
3. Enter the `API Key` in `ZOOM_KEY`, `API Secret` in `ZOOM SECRET`
4. Follow the link: https://api.zoom.us/developer/api/playground
5. In the API Endpoint field, select https://api.zoom.us/v1/chat/list
6. Enter the `Host User ID` in `ZOOM_HOST_ID`


Step 2 - Set up Youtube
-------------------------

Add the following keys to the `.env` file

    GOOGLE_REFRESH_TOKEN
    GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET

To get the keys, follow these steps:
1. Go to the developer console: https://console.developers.google.com/cloud-resource-manager
2. Create a new project and go to the new project
3. Follow the link: https://console.developers.google.com/apis/api/youtube.googleapis.com/overview
4. Turn on `YouTube Data API v3`
5. Follow the link: https://console.developers.google.com/apis/credentials
6. create OAuth client credentials.
7. Select `Desktop` as type of application, create
8. Enter `Client ID` in `GOOGLE_CLIENT_ID` and `Client Secret` in `GOOGLE_CLIENT_SECRET`

To get the `GOOGLE_REFRESH_TOKEN` follow these steps:

1. Follow the link: [https://accounts.google.com/o/oauth2/auth?client_id=<GOOGLE_CLIENT_ID>&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&access_type=offline&response_type=code](https://accounts.google.com/o/oauth2/auth?client_id=<MY_CLIENT_ID>&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope=https://www.googleapis.com/auth/youtube.upload&access_type=offline&response_type=code), **replacing** `<GOOGLE_CLIENT_ID>` with the `GOOGLE_CLIENT_ID`, you got from the previous step
2. Select the Google account you need access for
3. Get access
4. Enter the token in the .env file, in the `.env` in the `GOOGLE_CODE` field
5. Run the following script 
```
    $ python3.6 src/get_google_refresh_token.py`
```
6. Enter the refresh token in the `.env` file, in the `GOOGLE_REFRESH_TOKEN` field


Step 3 - Set up Slack
-----------------------

Add the following keys to the `.env` file

    SLACK_CHANNEL
    SLACK_TOKEN

1. Enter the recipients (separated with commas) in `SLACK_CHANNEL`, for example `SLACK_CHANNEL=#my_cannel,@my_user`
2. Enter the slack token in `SLACK_TOKEN`

Step 4 - AirTable keys
-----------------------
1. `AIR_TABLE_API_KEY`: Airtable api key from personal account
2. `AIR_TABLE_BASE_KEY`: Unique key to identify airtable base.

Step 5 - Check keys
-----------------------

To make sure all the keys were entered into the `.env` file, run the script in docker container
```
    $ docker-compose run app bash
    $ python3.6 src/check_env.py
```


Step 6 - Run the app
-------------------------

Build the image as specified by Dockerfile and run the container to launch the app.


Sample .env file
-----------------

```
ZOOM_KEY=AAAAAAAAAAAAAAA
ZOOM_SECRET=BBBBBBBBBBBB
ZOOM_HOST_ID=CCCCCCCCCCC
ZOOM_EMAIL=mail@gmail.com
ZOOM_PASSWORD=user_password

GOOGLE_CLIENT_ID=AAAAAAAAAAAAAA.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=BBBBBBBBBBBBBb
GOOGLE_REFRESH_TOKEN=CCCCCCCCCCCC
GOOGLE_CODE=DDDDDDDDDDDDDD

SLACK_CHANNEL=@user
SLACK_TOKEN=AAAAAAAAAAAAA

AIR_TABLE_API_KEY=keyAAAAAAAAAAAAAAA
AIR_TABLE_BASE_KEY=appAAAAAAAA
AIR_TABLE_TABLE_NAME=Zoom Recordings
AIR_TABLE_TABLE_COLUMNS=Recording Title,Youtube link
```


License
-------

[The MIT License (MIT)](https://en.wikipedia.org/wiki/MIT_License)
