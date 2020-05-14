# -*- coding: utf-8 -*-

import os.path

from settings import (
    ZOOM_KEY,
    ZOOM_SECRET,
    ZOOM_HOST_ID,
    ZOOM_EMAIL,
    ZOOM_PASSWORD,
    VIDEO_DIR,
    GOOGLE_REFRESH_TOKEN,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    DOWNLOADED_FILES,
    LOCK_FILE,
    MIN_DURATION,
    FILTER_MEETING_BY_NAME,
    ONLY_MEETING_NAMES,
)
from youtube import YoutubeRecording
from zoom import ZoomRecording


class lock(object):
    def __init__(self, lock_file):
        self._lock_file = lock_file

    def __enter__(self):
        if os.path.exists(self._lock_file):
            exit('The program is still running')
        open(self._lock_file, 'w').close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self._lock_file):
            os.remove(self._lock_file)


if __name__ == '__main__':
    with lock(LOCK_FILE):
        print('Start...')
        # download videos from zoom
        zoom = ZoomRecording(
            ZOOM_KEY,
            ZOOM_SECRET,
            ZOOM_HOST_ID,
            duration_min=MIN_DURATION,
            filter_meeting_by_name=FILTER_MEETING_BY_NAME,
            only_meeting_names=ONLY_MEETING_NAMES,
        )

        zoom.download_meetings(
            ZOOM_EMAIL,
            ZOOM_PASSWORD,
            VIDEO_DIR,
            DOWNLOADED_FILES
        )

        # upload videos to youtube
        youtube = YoutubeRecording(
            GOOGLE_CLIENT_ID,
            GOOGLE_CLIENT_SECRET,
            GOOGLE_REFRESH_TOKEN,
            video_handler_class=None
        )
        youtube.upload_from_dir(VIDEO_DIR)
        print('End.')
