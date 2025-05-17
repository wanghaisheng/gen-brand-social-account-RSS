import os
from pytubefix import Channel,YouTube

folder_path = "./result"
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

URL = os.getenv("URL")
URL=URL.split('.com/')[-1]
import html
import json
import re
from typing import List, Tuple

import requests

# Constants
RE_YOUTUBE = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
RE_XML_TRANSCRIPT = r'<text start="([^"]*)" dur="([^"]*)">([^<]*)<\/text>'


# Custom Exception Classes
class YoutubeTranscriptError(Exception):
    """Base class for YouTube transcript exceptions"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(f"[YoutubeTranscript] 🚨 {message}")


class YoutubeTranscriptTooManyRequestError(YoutubeTranscriptError):
    """Raised when YouTube is receiving too many requests"""
    pass


class YoutubeTranscriptVideoUnavailableError(YoutubeTranscriptError):
    """Raised when the video is no longer available"""

    def __init__(self, message: str, video_id: str):
        self.video_id = video_id
        super().__init__(message)


class YoutubeTranscriptDisabledError(YoutubeTranscriptError):
    """Raised when transcript is disabled on the video"""

    def __init__(self, message: str, video_id: str):
        self.video_id = video_id
        super().__init__(message)


class YoutubeTranscriptNotAvailableError(YoutubeTranscriptError):
    """Raised when no transcripts are available for the video"""

    def __init__(self, message: str, video_id: str):
        self.video_id = video_id
        super().__init__(message)


class YoutubeTranscriptNotAvailableLanguageError(YoutubeTranscriptError):
    """Raised when transcript is not available in the requested language"""

    def __init__(self, message: str, lang: str, available_langs: List[str], video_id: str):
        self.lang = lang
        self.available_langs = available_langs
        self.video_id = video_id
        super().__init__(message)


class TranscriptResponse:
    """Class to represent a transcript response"""

    def __init__(self, text: str, duration: float, offset: float, lang: str = ""):
        self.text = text
        self.duration = duration
        self.offset = offset
        self.lang = lang


class YoutubeTranscript:
    """Class to fetch transcripts from YouTube videos"""

    @staticmethod
    def retrieve_video_id(video_id: str) -> str:
        """Extract YouTube video ID from a string (URL or ID)"""
        if len(video_id) == 11:
            return video_id

        match = re.search(RE_YOUTUBE, video_id)
        if match:
            return match.group(1)

        raise YoutubeTranscriptError("Impossible to retrieve Youtube video ID.")

    @staticmethod
    def decode_html(text: str) -> str:
        """Decode HTML entities in text"""
        # Replace specific encoded strings
        text = text.replace("&amp;#39;", "'")
        # Use html.unescape for all other entities
        return html.unescape(text)

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize a filename to make it safe for file systems"""
        # Decode HTML entities
        filename = html.unescape(filename)

        # Replace illegal characters
        filename = re.sub(r'[<>:"/\\|? *]', "_", filename)

        # Remove leading/trailing spaces and dots
        filename = filename.strip(" .")

        # Limit length
        if len(filename) > 200:
            filename = filename[:200]

        return filename

    def fetch_transcript(self, video_id: str, lang: str = "") -> Tuple[List[TranscriptResponse], str]:
        """
        Fetch transcript for a YouTube video

        Args:
            video_id: YouTube video ID or URL
            lang: Language code (optional)

        Returns:
            Tuple of (transcript_items, video_title)

        Raises:
            Various YoutubeTranscriptError exceptions
        """
        # Extract video ID if URL was provided
        identifier = self.retrieve_video_id(video_id)

        # Create a session with headers
        session = requests.Session()
        session.headers.update({"User-Agent": USER_AGENT})

        # Fetch the video page
        video_page_url = f"https://www.youtube.com/watch?v={identifier}"
        response = session.get(video_page_url)

        if response.status_code != 200:
            raise YoutubeTranscriptVideoUnavailableError(
                f"Failed to fetch video page (HTTP {response.status_code})",
                identifier
            )

        video_page_html = response.text

        # Extract video title
        title_match = re.search(r'<title>(.+?) - YouTube</title>', video_page_html)
        video_title = ""
        if title_match:
            video_title = html.unescape(title_match.group(1))

        # Look for captions data
        if '"captions":' not in video_page_html:
            if 'class="g-recaptcha"' in video_page_html:
                raise YoutubeTranscriptTooManyRequestError(
                    "YouTube is receiving too many requests from this IP and now requires solving a captcha to continue"
                )
            if '"playabilityStatus":' not in video_page_html:
                raise YoutubeTranscriptVideoUnavailableError(
                    f"The video is no longer available ({identifier})",
                    identifier
                )
            raise YoutubeTranscriptDisabledError(
                f"Transcript is disabled on this video ({identifier})",
                identifier
            )

        # Extract captions data
        captions_data = video_page_html.split('"captions":')[1]
        captions_data = captions_data.split(',"videoDetails')[0]

        try:
            captions_json = json.loads('{' + '"captions":' + captions_data + '}')
            caption_tracks = captions_json.get('captions', {}).get('playerCaptionsTracklistRenderer', {}).get(
                'captionTracks', [])
        except json.JSONDecodeError:
            raise YoutubeTranscriptDisabledError(
                f"Failed to parse captions data for video ({identifier})",
                identifier
            )

        if not caption_tracks:
            raise YoutubeTranscriptNotAvailableError(
                f"No transcripts are available for this video ({identifier})",
                identifier
            )

        # Select the appropriate caption track
        transcript_url = None
        if lang:
            # Find the requested language
            for track in caption_tracks:
                if track.get('languageCode') == lang:
                    transcript_url = track.get('baseUrl')
                    break

            if not transcript_url:
                # Language not found
                available_langs = [track.get('languageCode') for track in caption_tracks]
                raise YoutubeTranscriptNotAvailableLanguageError(
                    f"No transcripts are available in {lang} for this video ({identifier}). Available languages: {', '.join(available_langs)}",
                    lang,
                    available_langs,
                    identifier
                )
        else:
            # Use the first available track
            transcript_url = caption_tracks[0].get('baseUrl')

        # Fetch the transcript XML
        transcript_response = session.get(transcript_url)

        if transcript_response.status_code != 200:
            raise YoutubeTranscriptNotAvailableError(
                f"Failed to fetch transcript (HTTP {transcript_response.status_code})",
                identifier
            )

        transcript_xml = transcript_response.text

        # Parse the XML to extract transcript items
        transcript_items = []

        matches = re.findall(RE_XML_TRANSCRIPT, transcript_xml)
        for match in matches:
            offset = float(match[0])
            duration = float(match[1])
            text = self.decode_html(match[2])

            transcript_items.append(TranscriptResponse(
                text=text,
                duration=duration,
                offset=offset,
                lang=lang
            ))

        return transcript_items, video_title

ytrans=YoutubeTranscript()


# https://youtubetotranscript.com/transcript
def gettransp():

  c = Channel(f"https://www.youtube.com/{URL}")
  print(f'Downloading videos by: {c.channel_name}')

  for video in c.videos:
      print('===',video)
      id=video.video_id

      videourl = f'http://youtube.com/watch?v={id}'
      yt = YouTube(videourl)

      print('srt',yt.captions)
      if not yt.captions=={}:
          caption = yt.captions['a.en']
          caption.save_captions(f"{id}.txt")
      else:
          print(f'there is no srt for {videourl}')
          try:
              transcript_items,title=ytrans.fetch_transcript(id,'en')
              print('===',transcript_items)
          except Exception as e:
              print(f'error :{e}')
gettransp()
