class YoutubeTabIE(YoutubeTabBaseInfoExtractor):
    IE_DESC = 'YouTube Tabs'
    _VALID_URL = r'''(?x:
        https?://
            (?!consent\.)(?:\w+\.)?
            (?:
                youtube(?:kids)?\.com|
                %(invidious)s
            )/
            (?:
                (?P<channel_type>channel|c|user|browse)/|
                (?P<not_channel>
                    feed/|hashtag/|
                    (?:playlist|watch)\?.*?\blist=
                )|
                (?!(?:%(reserved_names)s)\b)  # Direct URLs
            )
            (?P<id>[^/?\#&]+)
    )''' % {
        'reserved_names': YoutubeBaseInfoExtractor._RESERVED_NAMES,
        'invidious': '|'.join(YoutubeBaseInfoExtractor._INVIDIOUS_SITES),
    }
    IE_NAME = 'youtube:tab'

    _TESTS = [{
        'note': 'playlists, multipage',
        'url': 'https://www.youtube.com/c/ИгорьКлейнер/playlists?view=1&flow=grid',
        'playlist_mincount': 94,
        'info_dict': {
            'id': 'UCqj7Cz7revf5maW9g5pgNcg',
            'title': 'Igor Kleiner - Playlists',
            'description': 'md5:be97ee0f14ee314f1f002cf187166ee2',
            'uploader': 'Igor Kleiner',
            'uploader_id': '@IgorDataScience',
            'uploader_url': 'https://www.youtube.com/@IgorDataScience',
            'channel': 'Igor Kleiner',
            'channel_id': 'UCqj7Cz7revf5maW9g5pgNcg',
            'tags': ['"критическое', 'мышление"', '"наука', 'просто"', 'математика', '"анализ', 'данных"'],
            'channel_url': 'https://www.youtube.com/channel/UCqj7Cz7revf5maW9g5pgNcg',
            'channel_follower_count': int
        },
    }, {
        'note': 'playlists, multipage, different order',
        'url': 'https://www.youtube.com/user/igorkle1/playlists?view=1&sort=dd',
        'playlist_mincount': 94,
        'info_dict': {
            'id': 'UCqj7Cz7revf5maW9g5pgNcg',
            'title': 'Igor Kleiner - Playlists',
            'description': 'md5:be97ee0f14ee314f1f002cf187166ee2',
            'uploader': 'Igor Kleiner',
            'uploader_id': '@IgorDataScience',
            'uploader_url': 'https://www.youtube.com/@IgorDataScience',
            'tags': ['"критическое', 'мышление"', '"наука', 'просто"', 'математика', '"анализ', 'данных"'],
            'channel_id': 'UCqj7Cz7revf5maW9g5pgNcg',
            'channel': 'Igor Kleiner',
            'channel_url': 'https://www.youtube.com/channel/UCqj7Cz7revf5maW9g5pgNcg',
            'channel_follower_count': int
        },
    }, {
        'note': 'playlists, series',
        'url': 'https://www.youtube.com/c/3blue1brown/playlists?view=50&sort=dd&shelf_id=3',
        'playlist_mincount': 5,
        'info_dict': {
            'id': 'UCYO_jab_esuFRV4b17AJtAw',
            'title': '3Blue1Brown - Playlists',
            'description': 'md5:e1384e8a133307dd10edee76e875d62f',
            'channel_url': 'https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw',
            'channel': '3Blue1Brown',
            'channel_id': 'UCYO_jab_esuFRV4b17AJtAw',
            'uploader_id': '@3blue1brown',
            'uploader_url': 'https://www.youtube.com/@3blue1brown',
            'uploader': '3Blue1Brown',
            'tags': ['Mathematics'],
            'channel_follower_count': int
        },
    }, {
        'note': 'playlists, singlepage',
        'url': 'https://www.youtube.com/user/ThirstForScience/playlists',
        'playlist_mincount': 4,
        'info_dict': {
            'id': 'UCAEtajcuhQ6an9WEzY9LEMQ',
            'title': 'ThirstForScience - Playlists',
            'description': 'md5:609399d937ea957b0f53cbffb747a14c',
            'uploader': 'ThirstForScience',
            'uploader_url': 'https://www.youtube.com/@ThirstForScience',
            'uploader_id': '@ThirstForScience',
            'channel_id': 'UCAEtajcuhQ6an9WEzY9LEMQ',
            'channel_url': 'https://www.youtube.com/channel/UCAEtajcuhQ6an9WEzY9LEMQ',
            'tags': 'count:13',
            'channel': 'ThirstForScience',
            'channel_follower_count': int
        }
    }, {
        'url': 'https://www.youtube.com/c/ChristophLaimer/playlists',
        'only_matching': True,
    }, {
        'note': 'basic, single video playlist',
        'url': 'https://www.youtube.com/playlist?list=PL4lCao7KL_QFVb7Iudeipvc2BCavECqzc',
        'info_dict': {
            'id': 'PL4lCao7KL_QFVb7Iudeipvc2BCavECqzc',
            'title': 'youtube-dl public playlist',
            'description': '',
            'tags': [],
            'view_count': int,
            'modified_date': '20201130',
            'channel': 'Sergey M.',
            'channel_id': 'UCmlqkdCBesrv2Lak1mF_MxA',
            'channel_url': 'https://www.youtube.com/channel/UCmlqkdCBesrv2Lak1mF_MxA',
            'availability': 'public',
            'uploader': 'Sergey M.',
            'uploader_url': 'https://www.youtube.com/@sergeym.6173',
            'uploader_id': '@sergeym.6173',
        },
        'playlist_count': 1,
    }, {
        'note': 'empty playlist',
        'url': 'https://www.youtube.com/playlist?list=PL4lCao7KL_QFodcLWhDpGCYnngnHtQ-Xf',
        'info_dict': {
            'id': 'PL4lCao7KL_QFodcLWhDpGCYnngnHtQ-Xf',
            'title': 'youtube-dl empty playlist',
            'tags': [],
            'channel': 'Sergey M.',
            'description': '',
            'modified_date': '20160902',
            'channel_id': 'UCmlqkdCBesrv2Lak1mF_MxA',
            'channel_url': 'https://www.youtube.com/channel/UCmlqkdCBesrv2Lak1mF_MxA',
            'availability': 'public',
            'uploader_url': 'https://www.youtube.com/@sergeym.6173',
            'uploader_id': '@sergeym.6173',
            'uploader': 'Sergey M.',
        },
        'playlist_count': 0,
    }, {
        'note': 'Home tab',
        'url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w/featured',
        'info_dict': {
            'id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'title': 'lex will - Home',
            'description': 'md5:2163c5d0ff54ed5f598d6a7e6211e488',
            'uploader': 'lex will',
            'uploader_id': '@lexwill718',
            'channel': 'lex will',
            'tags': ['bible', 'history', 'prophesy'],
            'uploader_url': 'https://www.youtube.com/@lexwill718',
            'channel_url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w',
            'channel_id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'channel_follower_count': int
        },
        'playlist_mincount': 2,
    }, {
        'note': 'Videos tab',
        'url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w/videos',
        'info_dict': {
            'id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'title': 'lex will - Videos',
            'description': 'md5:2163c5d0ff54ed5f598d6a7e6211e488',
            'uploader': 'lex will',
            'uploader_id': '@lexwill718',
            'tags': ['bible', 'history', 'prophesy'],
            'channel_url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w',
            'channel_id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'uploader_url': 'https://www.youtube.com/@lexwill718',
            'channel': 'lex will',
            'channel_follower_count': int
        },
        'playlist_mincount': 975,
    }, {
        'note': 'Videos tab, sorted by popular',
        'url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w/videos?view=0&sort=p&flow=grid',
        'info_dict': {
            'id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'title': 'lex will - Videos',
            'description': 'md5:2163c5d0ff54ed5f598d6a7e6211e488',
            'uploader': 'lex will',
            'uploader_id': '@lexwill718',
            'channel_id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'uploader_url': 'https://www.youtube.com/@lexwill718',
            'channel': 'lex will',
            'tags': ['bible', 'history', 'prophesy'],
            'channel_url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w',
            'channel_follower_count': int
        },
        'playlist_mincount': 199,
    }, {
        'note': 'Playlists tab',
        'url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w/playlists',
        'info_dict': {
            'id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'title': 'lex will - Playlists',
            'description': 'md5:2163c5d0ff54ed5f598d6a7e6211e488',
            'uploader': 'lex will',
            'uploader_id': '@lexwill718',
            'uploader_url': 'https://www.youtube.com/@lexwill718',
            'channel': 'lex will',
            'channel_url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w',
            'channel_id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'tags': ['bible', 'history', 'prophesy'],
            'channel_follower_count': int
        },
        'playlist_mincount': 17,
    }, {
        'note': 'Community tab',
        'url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w/community',
        'info_dict': {
            'id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'title': 'lex will - Community',
            'description': 'md5:2163c5d0ff54ed5f598d6a7e6211e488',
            'channel': 'lex will',
            'channel_url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w',
            'channel_id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'tags': ['bible', 'history', 'prophesy'],
            'channel_follower_count': int,
            'uploader_url': 'https://www.youtube.com/@lexwill718',
            'uploader_id': '@lexwill718',
            'uploader': 'lex will',
        },
        'playlist_mincount': 18,
    }, {
        'note': 'Channels tab',
        'url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w/channels',
        'info_dict': {
            'id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'title': 'lex will - Channels',
            'description': 'md5:2163c5d0ff54ed5f598d6a7e6211e488',
            'channel': 'lex will',
            'channel_url': 'https://www.youtube.com/channel/UCKfVa3S1e4PHvxWcwyMMg8w',
            'channel_id': 'UCKfVa3S1e4PHvxWcwyMMg8w',
            'tags': ['bible', 'history', 'prophesy'],
            'channel_follower_count': int,
            'uploader_url': 'https://www.youtube.com/@lexwill718',
            'uploader_id': '@lexwill718',
            'uploader': 'lex will',
        },
        'playlist_mincount': 12,
    }, {
        'note': 'Search tab',
        'url': 'https://www.youtube.com/c/3blue1brown/search?query=linear%20algebra',
        'playlist_mincount': 40,
        'info_dict': {
            'id': 'UCYO_jab_esuFRV4b17AJtAw',
            'title': '3Blue1Brown - Search - linear algebra',
            'description': 'md5:e1384e8a133307dd10edee76e875d62f',
            'channel_url': 'https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw',
            'tags': ['Mathematics'],
            'channel': '3Blue1Brown',
            'channel_id': 'UCYO_jab_esuFRV4b17AJtAw',
            'channel_follower_count': int,
            'uploader_url': 'https://www.youtube.com/@3blue1brown',
            'uploader_id': '@3blue1brown',
            'uploader': '3Blue1Brown',
        },
    }, {
        'url': 'https://invidio.us/channel/UCmlqkdCBesrv2Lak1mF_MxA',
        'only_matching': True,
    }, {
        'url': 'https://www.youtubekids.com/channel/UCmlqkdCBesrv2Lak1mF_MxA',
        'only_matching': True,
    }, {
        'url': 'https://music.youtube.com/channel/UCmlqkdCBesrv2Lak1mF_MxA',
        'only_matching': True,
    }, {
        'note': 'Playlist with deleted videos (#651). As a bonus, the video #51 is also twice in this list.',
        'url': 'https://www.youtube.com/playlist?list=PLwP_SiAcdui0KVebT0mU9Apz359a4ubsC',
        'info_dict': {
            'title': '29C3: Not my department',
            'id': 'PLwP_SiAcdui0KVebT0mU9Apz359a4ubsC',
            'description': 'md5:a14dc1a8ef8307a9807fe136a0660268',
            'tags': [],
            'view_count': int,
            'modified_date': '20150605',
            'channel_id': 'UCEPzS1rYsrkqzSLNp76nrcg',
            'channel_url': 'https://www.youtube.com/channel/UCEPzS1rYsrkqzSLNp76nrcg',
            'channel': 'Christiaan008',
            'availability': 'public',
            'uploader_id': '@ChRiStIaAn008',
            'uploader': 'Christiaan008',
            'uploader_url': 'https://www.youtube.com/@ChRiStIaAn008',
        },
        'playlist_count': 96,
    }, {
        'note': 'Large playlist',
        'url': 'https://www.youtube.com/playlist?list=UUBABnxM4Ar9ten8Mdjj1j0Q',
        'info_dict': {
            'title': 'Uploads from Cauchemar',
            'id': 'UUBABnxM4Ar9ten8Mdjj1j0Q',
            'channel_url': 'https://www.youtube.com/channel/UCBABnxM4Ar9ten8Mdjj1j0Q',
            'tags': [],
            'modified_date': r're:\d{8}',
            'channel': 'Cauchemar',
            'view_count': int,
            'description': '',
            'channel_id': 'UCBABnxM4Ar9ten8Mdjj1j0Q',
            'availability': 'public',
            'uploader_id': '@Cauchemar89',
            'uploader': 'Cauchemar',
            'uploader_url': 'https://www.youtube.com/@Cauchemar89',
        },
        'playlist_mincount': 1123,
        'expected_warnings': [r'[Uu]navailable videos (are|will be) hidden'],
    }, {
        'note': 'even larger playlist, 8832 videos',
        'url': 'http://www.youtube.com/user/NASAgovVideo/videos',
        'only_matching': True,
    }, {
        'note': 'Buggy playlist: the webpage has a "Load more" button but it doesn\'t have more videos',
        'url': 'https://www.youtube.com/playlist?list=UUXw-G3eDE9trcvY2sBMM_aA',
        'info_dict': {
            'title': 'Uploads from Interstellar Movie',
            'id': 'UUXw-G3eDE9trcvY2sBMM_aA',
            'tags': [],
            'view_count': int,
            'channel_id': 'UCXw-G3eDE9trcvY2sBMM_aA',
            'channel_url': 'https://www.youtube.com/channel/UCXw-G3eDE9trcvY2sBMM_aA',
            'channel': 'Interstellar Movie',
            'description': '',
            'modified_date': r're:\d{8}',
            'availability': 'public',
            'uploader_id': '@InterstellarMovie',
            'uploader': 'Interstellar Movie',
            'uploader_url': 'https://www.youtube.com/@InterstellarMovie',
        },
        'playlist_mincount': 21,
    }, {
        'note': 'Playlist with "show unavailable videos" button',
        'url': 'https://www.youtube.com/playlist?list=UUTYLiWFZy8xtPwxFwX9rV7Q',
        'info_dict': {
            'title': 'Uploads from Phim Siêu Nhân Nhật Bản',
            'id': 'UUTYLiWFZy8xtPwxFwX9rV7Q',
            'view_count': int,
            'channel': 'Phim Siêu Nhân Nhật Bản',
            'tags': [],
            'description': '',
            'channel_url': 'https://www.youtube.com/channel/UCTYLiWFZy8xtPwxFwX9rV7Q',
            'channel_id': 'UCTYLiWFZy8xtPwxFwX9rV7Q',
            'modified_date': r're:\d{8}',
            'availability': 'public',
            'uploader_url': 'https://www.youtube.com/@phimsieunhannhatban',
            'uploader_id': '@phimsieunhannhatban',
            'uploader': 'Phim Siêu Nhân Nhật Bản',
        },
        'playlist_mincount': 200,
        'expected_warnings': [r'[Uu]navailable videos (are|will be) hidden'],
    }, {
        'note': 'Playlist with unavailable videos in page 7',
        'url': 'https://www.youtube.com/playlist?list=UU8l9frL61Yl5KFOl87nIm2w',
        'info_dict': {
            'title': 'Uploads from BlankTV',
            'id': 'UU8l9frL61Yl5KFOl87nIm2w',
            'channel': 'BlankTV',
            'channel_url': 'https://www.youtube.com/channel/UC8l9frL61Yl5KFOl87nIm2w',
            'channel_id': 'UC8l9frL61Yl5KFOl87nIm2w',
            'view_count': int,
            'tags': [],
            'modified_date': r're:\d{8}',
            'description': '',
            'availability': 'public',
            'uploader_id': '@blanktv',
            'uploader': 'BlankTV',
            'uploader_url': 'https://www.youtube.com/@blanktv',
        },
        'playlist_mincount': 1000,
        'expected_warnings': [r'[Uu]navailable videos (are|will be) hidden'],
    }, {
        'note': 'https://github.com/ytdl-org/youtube-dl/issues/21844',
        'url': 'https://www.youtube.com/playlist?list=PLzH6n4zXuckpfMu_4Ff8E7Z1behQks5ba',
        'info_dict': {
            'title': 'Data Analysis with Dr Mike Pound',
            'id': 'PLzH6n4zXuckpfMu_4Ff8E7Z1behQks5ba',
            'description': 'md5:7f567c574d13d3f8c0954d9ffee4e487',
            'tags': [],
            'view_count': int,
            'channel_id': 'UC9-y-6csu5WGm29I7JiwpnA',
            'channel_url': 'https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA',
            'channel': 'Computerphile',
            'availability': 'public',
            'modified_date': '20190712',
            'uploader_id': '@Computerphile',
            'uploader': 'Computerphile',
            'uploader_url': 'https://www.youtube.com/@Computerphile',
        },
        'playlist_mincount': 11,
    }, {
        'url': 'https://invidio.us/playlist?list=PL4lCao7KL_QFVb7Iudeipvc2BCavECqzc',
        'only_matching': True,
    }, {
        'note': 'Playlist URL that does not actually serve a playlist',
        'url': 'https://www.youtube.com/watch?v=FqZTN594JQw&list=PLMYEtVRpaqY00V9W81Cwmzp6N6vZqfUKD4',
        'info_dict': {
            'id': 'FqZTN594JQw',
            'ext': 'webm',
            'title': "Smiley's People 01 detective, Adventure Series, Action",
            'upload_date': '20150526',
            'license': 'Standard YouTube License',
            'description': 'md5:507cdcb5a49ac0da37a920ece610be80',
            'categories': ['People & Blogs'],
            'tags': list,
            'view_count': int,
            'like_count': int,
        },
        'params': {
            'skip_download': True,
        },
        'skip': 'This video is not available.',
        'add_ie': [YoutubeIE.ie_key()],
    }, {
        'url': 'https://www.youtubekids.com/watch?v=Agk7R8I8o5U&list=PUZ6jURNr1WQZCNHF0ao-c0g',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/watch?v=MuAGGZNfUkU&list=RDMM',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/channel/UCoMdktPbSTixAyNGwb-UYkQ/live',
        'info_dict': {
            'id': 'AlTsmyW4auo',  # This will keep changing
            'ext': 'mp4',
            'title': str,
            'upload_date': r're:\d{8}',
            'description': str,
            'categories': ['News & Politics'],
            'tags': list,
            'like_count': int,
            'release_timestamp': int,
            'channel': 'Sky News',
            'channel_id': 'UCoMdktPbSTixAyNGwb-UYkQ',
            'age_limit': 0,
            'view_count': int,
            'thumbnail': r're:https?://i\.ytimg\.com/vi/[^/]+/maxresdefault(?:_live)?\.jpg',
            'playable_in_embed': True,
            'release_date': r're:\d+',
            'availability': 'public',
            'live_status': 'is_live',
            'channel_url': 'https://www.youtube.com/channel/UCoMdktPbSTixAyNGwb-UYkQ',
            'channel_follower_count': int,
            'concurrent_view_count': int,
            'uploader_url': 'https://www.youtube.com/@SkyNews',
            'uploader_id': '@SkyNews',
            'uploader': 'Sky News',
        },
        'params': {
            'skip_download': True,
        },
        'expected_warnings': ['Ignoring subtitle tracks found in '],
    }, {
        'url': 'https://www.youtube.com/user/TheYoungTurks/live',
        'info_dict': {
            'id': 'a48o2S1cPoo',
            'ext': 'mp4',
            'title': 'The Young Turks - Live Main Show',
            'upload_date': '20150715',
            'license': 'Standard YouTube License',
            'description': 'md5:438179573adcdff3c97ebb1ee632b891',
            'categories': ['News & Politics'],
            'tags': ['Cenk Uygur (TV Program Creator)', 'The Young Turks (Award-Winning Work)', 'Talk Show (TV Genre)'],
            'like_count': int,
        },
        'params': {
            'skip_download': True,
        },
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/channel/UC1yBKRuGpC1tSM73A0ZjYjQ/live',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/c/CommanderVideoHq/live',
        'only_matching': True,
    }, {
        'note': 'A channel that is not live. Should raise error',
        'url': 'https://www.youtube.com/user/numberphile/live',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/feed/trending',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/feed/library',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/feed/history',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/feed/subscriptions',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/feed/watch_later',
        'only_matching': True,
    }, {
        'note': 'Recommended - redirects to home page.',
        'url': 'https://www.youtube.com/feed/recommended',
        'only_matching': True,
    }, {
        'note': 'inline playlist with not always working continuations',
        'url': 'https://www.youtube.com/watch?v=UC6u0Tct-Fo&list=PL36D642111D65BE7C',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/course',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/zsecurity',
        'only_matching': True,
    }, {
        'url': 'http://www.youtube.com/NASAgovVideo/videos',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/TheYoungTurks/live',
        'only_matching': True,
    }, {
        'url': 'https://www.youtube.com/hashtag/cctv9',
        'info_dict': {
            'id': 'cctv9',
            'title': '#cctv9',
            'tags': [],
        },
        'playlist_mincount': 300,  # not consistent but should be over 300
    }, {
        'url': 'https://www.youtube.com/watch?list=PLW4dVinRY435CBE_JD3t-0SRXKfnZHS1P&feature=youtu.be&v=M9cJMXmQ_ZU',
        'only_matching': True,
    }, {
        'note': 'Requires Premium: should request additional YTM-info webpage (and have format 141) for videos in playlist',
        'url': 'https://music.youtube.com/playlist?list=PLRBp0Fe2GpgmgoscNFLxNyBVSFVdYmFkq',
        'only_matching': True
    }, {
        'note': '/browse/ should redirect to /channel/',
        'url': 'https://music.youtube.com/browse/UC1a8OFewdjuLq6KlF8M_8Ng',
        'only_matching': True
    }, {
        'note': 'VLPL, should redirect to playlist?list=PL...',
        'url': 'https://music.youtube.com/browse/VLPLRBp0Fe2GpgmgoscNFLxNyBVSFVdYmFkq',
        'info_dict': {
            'id': 'PLRBp0Fe2GpgmgoscNFLxNyBVSFVdYmFkq',
            'description': 'Providing you with copyright free / safe music for gaming, live streaming, studying and more!',
            'title': 'NCS : All Releases 💿',
            'channel_url': 'https://www.youtube.com/channel/UC_aEa8K-EOJ3D6gOs7HcyNg',
            'modified_date': r're:\d{8}',
            'view_count': int,
            'channel_id': 'UC_aEa8K-EOJ3D6gOs7HcyNg',
            'tags': [],
            'channel': 'NoCopyrightSounds',
            'availability': 'public',
            'uploader_url': 'https://www.youtube.com/@NoCopyrightSounds',
            'uploader': 'NoCopyrightSounds',
            'uploader_id': '@NoCopyrightSounds',
        },
        'playlist_mincount': 166,
        'expected_warnings': [r'[Uu]navailable videos (are|will be) hidden', 'YouTube Music is not directly supported'],
    }, {
        # TODO: fix 'unviewable' issue with this playlist when reloading with unavailable videos
        'note': 'Topic, should redirect to playlist?list=UU...',
        'url': 'https://music.youtube.com/browse/UC9ALqqC4aIeG5iDs7i90Bfw',
        'info_dict': {
            'id': 'UU9ALqqC4aIeG5iDs7i90Bfw',
            'title': 'Uploads from Royalty Free Music - Topic',
            'tags': [],
            'channel_id': 'UC9ALqqC4aIeG5iDs7i90Bfw',
            'channel': 'Royalty Free Music - Topic',
            'view_count': int,
            'channel_url': 'https://www.youtube.com/channel/UC9ALqqC4aIeG5iDs7i90Bfw',
            'modified_date': r're:\d{8}',
            'description': '',
            'availability': 'public',
            'uploader': 'Royalty Free Music - Topic',
        },
        'playlist_mincount': 101,
        'expected_warnings': ['YouTube Music is not directly supported', r'[Uu]navailable videos (are|will be) hidden'],
    }, {
        # Destination channel with only a hidden self tab (tab id is UCtFRv9O2AHqOZjjynzrv-xg)
        # Treat as a general feed
        'url': 'https://www.youtube.com/channel/UCtFRv9O2AHqOZjjynzrv-xg',
        'info_dict': {
            'id': 'UCtFRv9O2AHqOZjjynzrv-xg',
            'title': 'UCtFRv9O2AHqOZjjynzrv-xg',
            'tags': [],
        },
        'playlist_mincount': 9,
    }, {
        'note': 'Youtube music Album',
        'url': 'https://music.youtube.com/browse/MPREb_gTAcphH99wE',
        'info_dict': {
            'id': 'OLAK5uy_l1m0thk3g31NmIIz_vMIbWtyv7eZixlH0',
            'title': 'Album - Royalty Free Music Library V2 (50 Songs)',
            'tags': [],
            'view_count': int,
            'description': '',
            'availability': 'unlisted',
            'modified_date': r're:\d{8}',
        },
        'playlist_count': 50,
        'expected_warnings': ['YouTube Music is not directly supported'],
    }, {
        'note': 'unlisted single video playlist',
        'url': 'https://www.youtube.com/playlist?list=PLwL24UFy54GrB3s2KMMfjZscDi1x5Dajf',
        'info_dict': {
            'id': 'PLwL24UFy54GrB3s2KMMfjZscDi1x5Dajf',
            'title': 'yt-dlp unlisted playlist test',
            'availability': 'unlisted',
            'tags': [],
            'modified_date': '20220418',
            'channel': 'colethedj',
            'view_count': int,
            'description': '',
            'channel_id': 'UC9zHu_mHU96r19o-wV5Qs1Q',
            'channel_url': 'https://www.youtube.com/channel/UC9zHu_mHU96r19o-wV5Qs1Q',
            'uploader_url': 'https://www.youtube.com/@colethedj1894',
            'uploader_id': '@colethedj1894',
            'uploader': 'colethedj',
        },
        'playlist': [{
            'info_dict': {
                'title': 'youtube-dl test video "\'/\\ä↭𝕐',
                'id': 'BaW_jenozKc',
                '_type': 'url',
                'ie_key': 'Youtube',
                'duration': 10,
                'channel_id': 'UCLqxVugv74EIW3VWh2NOa3Q',
                'channel_url': 'https://www.youtube.com/channel/UCLqxVugv74EIW3VWh2NOa3Q',
                'view_count': int,
                'url': 'https://www.youtube.com/watch?v=BaW_jenozKc',
                'channel': 'Philipp Hagemeister',
                'uploader_id': '@PhilippHagemeister',
                'uploader_url': 'https://www.youtube.com/@PhilippHagemeister',
                'uploader': 'Philipp Hagemeister',
            }
        }],
        'playlist_count': 1,
        'params': {'extract_flat': True},
    }, {
        'note': 'API Fallback: Recommended - redirects to home page. Requires visitorData',
        'url': 'https://www.youtube.com/feed/recommended',
        'info_dict': {
            'id': 'recommended',
            'title': 'recommended',
            'tags': [],
        },
        'playlist_mincount': 50,
        'params': {
            'skip_download': True,
            'extractor_args': {'youtubetab': {'skip': ['webpage']}}
        },
    }, {
        'note': 'API Fallback: /videos tab, sorted by oldest first',
        'url': 'https://www.youtube.com/user/theCodyReeder/videos?view=0&sort=da&flow=grid',
        'info_dict': {
            'id': 'UCu6mSoMNzHQiBIOCkHUa2Aw',
            'title': 'Cody\'sLab - Videos',
            'description': 'md5:d083b7c2f0c67ee7a6c74c3e9b4243fa',
            'channel': 'Cody\'sLab',
            'channel_id': 'UCu6mSoMNzHQiBIOCkHUa2Aw',
            'tags': [],
            'channel_url': 'https://www.youtube.com/channel/UCu6mSoMNzHQiBIOCkHUa2Aw',
            'channel_follower_count': int
        },
        'playlist_mincount': 650,
        'params': {
            'skip_download': True,
            'extractor_args': {'youtubetab': {'skip': ['webpage']}}
        },
        'skip': 'Query for sorting no longer works',
    }, {
        'note': 'API Fallback: Topic, should redirect to playlist?list=UU...',
        'url': 'https://music.youtube.com/browse/UC9ALqqC4aIeG5iDs7i90Bfw',
        'info_dict': {
            'id': 'UU9ALqqC4aIeG5iDs7i90Bfw',
            'title': 'Uploads from Royalty Free Music - Topic',
            'modified_date': r're:\d{8}',
            'channel_id': 'UC9ALqqC4aIeG5iDs7i90Bfw',
            'description': '',
            'channel_url': 'https://www.youtube.com/channel/UC9ALqqC4aIeG5iDs7i90Bfw',
            'tags': [],
            'channel': 'Royalty Free Music - Topic',
            'view_count': int,
            'availability': 'public',
            'uploader': 'Royalty Free Music - Topic',
        },
        'playlist_mincount': 101,
        'params': {
            'skip_download': True,
            'extractor_args': {'youtubetab': {'skip': ['webpage']}}
        },
        'expected_warnings': ['YouTube Music is not directly supported', r'[Uu]navailable videos (are|will be) hidden'],
    }, {
        'note': 'non-standard redirect to regional channel',
        'url': 'https://www.youtube.com/channel/UCwVVpHQ2Cs9iGJfpdFngePQ',
        'only_matching': True
    }, {
        'note': 'collaborative playlist (uploader name in the form "by <uploader> and x other(s)")',
        'url': 'https://www.youtube.com/playlist?list=PLx-_-Kk4c89oOHEDQAojOXzEzemXxoqx6',
        'info_dict': {
            'id': 'PLx-_-Kk4c89oOHEDQAojOXzEzemXxoqx6',
            'modified_date': '20220407',
            'channel_url': 'https://www.youtube.com/channel/UCKcqXmCcyqnhgpA5P0oHH_Q',
            'tags': [],
            'availability': 'unlisted',
            'channel_id': 'UCKcqXmCcyqnhgpA5P0oHH_Q',
            'channel': 'pukkandan',
            'description': 'Test for collaborative playlist',
            'title': 'yt-dlp test - collaborative playlist',
            'view_count': int,
            'uploader_url': 'https://www.youtube.com/@pukkandan',
            'uploader_id': '@pukkandan',
            'uploader': 'pukkandan',
        },
        'playlist_mincount': 2
    }, {
        'note': 'translated tab name',
        'url': 'https://www.youtube.com/channel/UCiu-3thuViMebBjw_5nWYrA/playlists',
        'info_dict': {
            'id': 'UCiu-3thuViMebBjw_5nWYrA',
            'tags': [],
            'channel_url': 'https://www.youtube.com/channel/UCiu-3thuViMebBjw_5nWYrA',
            'description': 'test description',
            'title': 'cole-dlp-test-acc - 再生リスト',
            'channel_id': 'UCiu-3thuViMebBjw_5nWYrA',
            'channel': 'cole-dlp-test-acc',
            'uploader_url': 'https://www.youtube.com/@coletdjnz',
            'uploader_id': '@coletdjnz',
            'uploader': 'cole-dlp-test-acc',
        },
        'playlist_mincount': 1,
        'params': {'extractor_args': {'youtube': {'lang': ['ja']}}},
        'expected_warnings': ['Preferring "ja"'],
    }, {
        # XXX: this should really check flat playlist entries, but the test suite doesn't support that
        'note': 'preferred lang set with playlist with translated video titles',
        'url': 'https://www.youtube.com/playlist?list=PLt5yu3-wZAlQAaPZ5Z-rJoTdbT-45Q7c0',
        'info_dict': {
            'id': 'PLt5yu3-wZAlQAaPZ5Z-rJoTdbT-45Q7c0',
            'tags': [],
            'view_count': int,
            'channel_url': 'https://www.youtube.com/channel/UCiu-3thuViMebBjw_5nWYrA',
            'channel': 'cole-dlp-test-acc',
            'channel_id': 'UCiu-3thuViMebBjw_5nWYrA',
            'description': 'test',
            'title': 'dlp test playlist',
            'availability': 'public',
            'uploader_url': 'https://www.youtube.com/@coletdjnz',
            'uploader_id': '@coletdjnz',
            'uploader': 'cole-dlp-test-acc',
        },
        'playlist_mincount': 1,
        'params': {'extractor_args': {'youtube': {'lang': ['ja']}}},
        'expected_warnings': ['Preferring "ja"'],
    }, {
        # shorts audio pivot for 2GtVksBMYFM.
        'url': 'https://www.youtube.com/feed/sfv_audio_pivot?bp=8gUrCikSJwoLMkd0VmtzQk1ZRk0SCzJHdFZrc0JNWUZNGgsyR3RWa3NCTVlGTQ==',
        'info_dict': {
            'id': 'sfv_audio_pivot',
            'title': 'sfv_audio_pivot',
            'tags': [],
        },
        'playlist_mincount': 50,

    }, {
        # Channel with a real live tab (not to be mistaken with streams tab)
        # Do not treat like it should redirect to live stream
        'url': 'https://www.youtube.com/channel/UCEH7P7kyJIkS_gJf93VYbmg/live',
        'info_dict': {
            'id': 'UCEH7P7kyJIkS_gJf93VYbmg',
            'title': 'UCEH7P7kyJIkS_gJf93VYbmg - Live',
            'tags': [],
        },
        'playlist_mincount': 20,
    }, {
        # Tab name is not the same as tab id
        'url': 'https://www.youtube.com/channel/UCQvWX73GQygcwXOTSf_VDVg/letsplay',
        'info_dict': {
            'id': 'UCQvWX73GQygcwXOTSf_VDVg',
            'title': 'UCQvWX73GQygcwXOTSf_VDVg - Let\'s play',
            'tags': [],
        },
        'playlist_mincount': 8,
    }, {
        # Home tab id is literally home. Not to get mistaken with featured
        'url': 'https://www.youtube.com/channel/UCQvWX73GQygcwXOTSf_VDVg/home',
        'info_dict': {
            'id': 'UCQvWX73GQygcwXOTSf_VDVg',
            'title': 'UCQvWX73GQygcwXOTSf_VDVg - Home',
            'tags': [],
        },
        'playlist_mincount': 8,
    }, {
        # Should get three playlists for videos, shorts and streams tabs
        'url': 'https://www.youtube.com/channel/UCK9V2B22uJYu3N7eR_BT9QA',
        'info_dict': {
            'id': 'UCK9V2B22uJYu3N7eR_BT9QA',
            'title': 'Polka Ch. 尾丸ポルカ',
            'channel_follower_count': int,
            'channel_id': 'UCK9V2B22uJYu3N7eR_BT9QA',
            'channel_url': 'https://www.youtube.com/channel/UCK9V2B22uJYu3N7eR_BT9QA',
            'description': 'md5:e56b74b5bb7e9c701522162e9abfb822',
            'channel': 'Polka Ch. 尾丸ポルカ',
            'tags': 'count:35',
            'uploader_url': 'https://www.youtube.com/@OmaruPolka',
            'uploader': 'Polka Ch. 尾丸ポルカ',
            'uploader_id': '@OmaruPolka',
        },
        'playlist_count': 3,
    }, {
        # Shorts tab with channel with handle
        # TODO: fix channel description
        'url': 'https://www.youtube.com/@NotJustBikes/shorts',
        'info_dict': {
            'id': 'UC0intLFzLaudFG-xAvUEO-A',
            'title': 'Not Just Bikes - Shorts',
            'tags': 'count:12',
            'channel_url': 'https://www.youtube.com/channel/UC0intLFzLaudFG-xAvUEO-A',
            'description': 'md5:26bc55af26855a608a5cf89dfa595c8d',
            'channel_follower_count': int,
            'channel_id': 'UC0intLFzLaudFG-xAvUEO-A',
            'channel': 'Not Just Bikes',
            'uploader_url': 'https://www.youtube.com/@NotJustBikes',
            'uploader': 'Not Just Bikes',
            'uploader_id': '@NotJustBikes',
        },
        'playlist_mincount': 10,
    }, {
        # Streams tab
        'url': 'https://www.youtube.com/channel/UC3eYAvjCVwNHgkaGbXX3sig/streams',
        'info_dict': {
            'id': 'UC3eYAvjCVwNHgkaGbXX3sig',
            'title': '中村悠一 - Live',
            'tags': 'count:7',
            'channel_id': 'UC3eYAvjCVwNHgkaGbXX3sig',
            'channel_url': 'https://www.youtube.com/channel/UC3eYAvjCVwNHgkaGbXX3sig',
            'channel': '中村悠一',
            'channel_follower_count': int,
            'description': 'md5:e744f6c93dafa7a03c0c6deecb157300',
            'uploader_url': 'https://www.youtube.com/@Yuichi-Nakamura',
            'uploader_id': '@Yuichi-Nakamura',
            'uploader': '中村悠一',
        },
        'playlist_mincount': 60,
    }, {
        # Channel with no uploads and hence no videos, streams, shorts tabs or uploads playlist. This should fail.
        # See test_youtube_lists
        'url': 'https://www.youtube.com/channel/UC2yXPzFejc422buOIzn_0CA',
        'only_matching': True,
    }, {
        # No uploads and no UCID given. Should fail with no uploads error
        # See test_youtube_lists
        'url': 'https://www.youtube.com/news',
        'only_matching': True
    }, {
        # No videos tab but has a shorts tab
        'url': 'https://www.youtube.com/c/TKFShorts',
        'info_dict': {
            'id': 'UCgJ5_1F6yJhYLnyMszUdmUg',
            'title': 'Shorts Break - Shorts',
            'tags': 'count:48',
            'channel_id': 'UCgJ5_1F6yJhYLnyMszUdmUg',
            'channel': 'Shorts Break',
            'description': 'md5:6de33c5e7ba686e5f3efd4e19c7ef499',
            'channel_follower_count': int,
            'channel_url': 'https://www.youtube.com/channel/UCgJ5_1F6yJhYLnyMszUdmUg',
            'uploader_url': 'https://www.youtube.com/@ShortsBreak_Official',
            'uploader': 'Shorts Break',
            'uploader_id': '@ShortsBreak_Official',
        },
        'playlist_mincount': 30,
    }, {
        # Trending Now Tab. tab id is empty
        'url': 'https://www.youtube.com/feed/trending',
        'info_dict': {
            'id': 'trending',
            'title': 'trending - Now',
            'tags': [],
        },
        'playlist_mincount': 30,
    }, {
        # Trending Gaming Tab. tab id is empty
        'url': 'https://www.youtube.com/feed/trending?bp=4gIcGhpnYW1pbmdfY29ycHVzX21vc3RfcG9wdWxhcg%3D%3D',
        'info_dict': {
            'id': 'trending',
            'title': 'trending - Gaming',
            'tags': [],
        },
        'playlist_mincount': 30,
    }, {
        # Shorts url result in shorts tab
        # TODO: Fix channel id extraction
        'url': 'https://www.youtube.com/channel/UCiu-3thuViMebBjw_5nWYrA/shorts',
        'info_dict': {
            'id': 'UCiu-3thuViMebBjw_5nWYrA',
            'title': 'cole-dlp-test-acc - Shorts',
            'channel': 'cole-dlp-test-acc',
            'description': 'test description',
            'channel_id': 'UCiu-3thuViMebBjw_5nWYrA',
            'channel_url': 'https://www.youtube.com/channel/UCiu-3thuViMebBjw_5nWYrA',
            'tags': [],
            'uploader_url': 'https://www.youtube.com/@coletdjnz',
            'uploader_id': '@coletdjnz',
            'uploader': 'cole-dlp-test-acc',
        },
        'playlist': [{
            'info_dict': {
                # Channel data is not currently available for short renderers (as of 2023-03-01)
                '_type': 'url',
                'ie_key': 'Youtube',
                'url': 'https://www.youtube.com/shorts/sSM9J5YH_60',
                'id': 'sSM9J5YH_60',
                'title': 'SHORT short',
                'view_count': int,
                'thumbnails': list,
            }
        }],
        'params': {'extract_flat': True},
    }, {
        # Live video status should be extracted
        'url': 'https://www.youtube.com/channel/UCQvWX73GQygcwXOTSf_VDVg/live',
        'info_dict': {
            'id': 'UCQvWX73GQygcwXOTSf_VDVg',
            'title': 'UCQvWX73GQygcwXOTSf_VDVg - Live',  # TODO, should be Minecraft - Live or Minecraft - Topic - Live
            'tags': []
        },
        'playlist': [{
            'info_dict': {
                '_type': 'url',
                'ie_key': 'Youtube',
                'url': 'startswith:https://www.youtube.com/watch?v=',
                'id': str,
                'title': str,
                'live_status': 'is_live',
                'channel_id': str,
                'channel_url': str,
                'concurrent_view_count': int,
                'channel': str,
                'uploader': str,
                'uploader_url': str,
                'uploader_id': str
            }
        }],
        'params': {'extract_flat': True, 'playlist_items': '1'},
        'playlist_mincount': 1
    }, {
        # Channel renderer metadata. Contains number of videos on the channel
        'url': 'https://www.youtube.com/channel/UCiu-3thuViMebBjw_5nWYrA/channels',
        'info_dict': {
            'id': 'UCiu-3thuViMebBjw_5nWYrA',
            'title': 'cole-dlp-test-acc - Channels',
            'channel': 'cole-dlp-test-acc',
            'description': 'test description',
            'channel_id': 'UCiu-3thuViMebBjw_5nWYrA',
            'channel_url': 'https://www.youtube.com/channel/UCiu-3thuViMebBjw_5nWYrA',
            'tags': [],
            'uploader_url': 'https://www.youtube.com/@coletdjnz',
            'uploader_id': '@coletdjnz',
            'uploader': 'cole-dlp-test-acc',
        },
        'playlist': [{
            'info_dict': {
                '_type': 'url',
                'ie_key': 'YoutubeTab',
                'url': 'https://www.youtube.com/channel/UC-lHJZR3Gqxm24_Vd_AJ5Yw',
                'id': 'UC-lHJZR3Gqxm24_Vd_AJ5Yw',
                'channel_id': 'UC-lHJZR3Gqxm24_Vd_AJ5Yw',
                'title': 'PewDiePie',
                'channel': 'PewDiePie',
                'channel_url': 'https://www.youtube.com/channel/UC-lHJZR3Gqxm24_Vd_AJ5Yw',
                'thumbnails': list,
                'channel_follower_count': int,
                'playlist_count': int,
                'uploader': 'PewDiePie',
                'uploader_url': 'https://www.youtube.com/@PewDiePie',
                'uploader_id': '@PewDiePie',
            }
        }],
        'params': {'extract_flat': True},
    }, {
        'url': 'https://www.youtube.com/@3blue1brown/about',
        'info_dict': {
            'id': 'UCYO_jab_esuFRV4b17AJtAw',
            'tags': ['Mathematics'],
            'title': '3Blue1Brown - About',
            'channel_follower_count': int,
            'channel_id': 'UCYO_jab_esuFRV4b17AJtAw',
            'channel': '3Blue1Brown',
            'view_count': int,
            'channel_url': 'https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw',
            'description': 'md5:e1384e8a133307dd10edee76e875d62f',
            'uploader_url': 'https://www.youtube.com/@3blue1brown',
            'uploader_id': '@3blue1brown',
            'uploader': '3Blue1Brown',
        },
        'playlist_count': 0,
    }, {
        # Podcasts tab, with rich entry playlistRenderers
        'url': 'https://www.youtube.com/@99percentinvisiblepodcast/podcasts',
        'info_dict': {
            'id': 'UCVMF2HD4ZgC0QHpU9Yq5Xrw',
            'channel_id': 'UCVMF2HD4ZgC0QHpU9Yq5Xrw',
            'uploader_url': 'https://www.youtube.com/@99percentinvisiblepodcast',
            'description': 'md5:3a0ed38f1ad42a68ef0428c04a15695c',
            'title': '99 Percent Invisible - Podcasts',
            'uploader': '99 Percent Invisible',
            'channel_follower_count': int,
            'channel_url': 'https://www.youtube.com/channel/UCVMF2HD4ZgC0QHpU9Yq5Xrw',
            'tags': [],
            'channel': '99 Percent Invisible',
            'uploader_id': '@99percentinvisiblepodcast',
        },
        'playlist_count': 1,
    }, {
        # Releases tab, with rich entry playlistRenderers (same as Podcasts tab)
        'url': 'https://www.youtube.com/@AHimitsu/releases',
        'info_dict': {
            'id': 'UCgFwu-j5-xNJml2FtTrrB3A',
            'channel': 'A Himitsu',
            'uploader_url': 'https://www.youtube.com/@AHimitsu',
            'title': 'A Himitsu - Releases',
            'uploader_id': '@AHimitsu',
            'uploader': 'A Himitsu',
            'channel_id': 'UCgFwu-j5-xNJml2FtTrrB3A',
            'tags': 'count:16',
            'description': 'I make music',
            'channel_url': 'https://www.youtube.com/channel/UCgFwu-j5-xNJml2FtTrrB3A',
            'channel_follower_count': int,
        },
        'playlist_mincount': 10,
    }]
