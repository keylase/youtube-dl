# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import (
    determine_ext
)


class WasdtvIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?wasd\.tv/channel/(?P<channelid>[0-9]+)/videos/(?P<id>[0-9]+)'
    _TESTS = [{
        'url': 'https://wasd.tv/channel/62946/videos/468561',
        'md5': '953d762d8075fcd86c2903c2673c975e',
        'info_dict': {
            'id': '468561',
            'ext': 'm3u8',
            'title': 'СИДИМ ДОМА И ГОТОВИМ ВМЕСТЕ С ВАМИ🍖IRL',
        }
    }, {
        'url': 'https://wasd.tv/channel/173869/videos/467794',
        'md5': '2ad3677093519aee5379ede68bc2120f',
        'info_dict': {
            'id': '467794',
            'ext': 'm3u8',
            'title': 'Новая Кыця / День отрыва #1',
        }
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        video_data = self._download_json(
            'https://wasd.tv/api/media-containers/%s' % video_id, video_id)

        title = video_data.get('result').get('media_container_name')

        formats = []
        media_container_streams = video_data['result'].get('media_container_streams', [])
        medium_url = media_container_streams[0]['stream_media'][0]['media_meta']['media_archive_url']
        ext = determine_ext(medium_url)
        if ext == 'm3u8':
            formats.extend(self._extract_m3u8_formats(
                medium_url, video_id, 'mp4', 'm3u8_native',
                m3u8_id='hls'))

        a_format = {
            'url': medium_url
        }
        formats.append(a_format)

        return {
            'id': video_id,
            'title': title,
            'formats': formats
        }
