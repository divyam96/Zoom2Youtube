from s3 import S3Sync

s3_sync = S3Sync()
s3_sync.s3_client.download_file('launchpadai', 'Zoom2YoutubeApp/config/.env', '/opt/app/.env')
