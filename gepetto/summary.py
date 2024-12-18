import re
import io
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import PyPDF2
from trafilatura import fetch_url, extract
from trafilatura.settings import DEFAULT_CONFIG
from copy import deepcopy

request_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "X-Browser-Channel": "stable",
    "X-Browser-Copyright": "Copyright 2024 Google LLC. All rights reserved."
}

def get_text_from_pdf(url: str) -> str:
    try:
        response = requests.get(url, headers=request_headers)
        file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Could not get pdf text for {url}")
        print(e)
        return "Could not extract text for this PDF.  Sorry."



def extract_video_id_and_trailing_text(input_string):
    # Use a regular expression to match a YouTube URL and extract the video ID
    video_id_match = re.search(r"https://www\.youtube\.com/watch\?v=([^&\s\?]+)", input_string)
    video_id = video_id_match.group(1) if video_id_match else None

    # If a video ID was found, remove the URL from the string to get the trailing text
    if video_id:
        url = video_id_match.group(0)  # The entire matched URL
        trailing_text = input_string.replace(url, '').strip()
    else:
        trailing_text = ''

    return video_id, trailing_text

async def get_text(url: str) -> str:
    page_text = ""
    if '//www.youtube.com/' in url:
        video_id, trailing_text = extract_video_id_and_trailing_text(url.strip("<>"))
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            return "Sorry, I couldn't get a transcript for that video."
        transcript_text = [x['text'] for x in transcript_list]
        page_text = ' '.join(transcript_text)
        if "The copyright belongs to Google LLC" in page_text:
            page_text = "Could not get the transcript - possibly I am being geoblocked"

    else:
        url_match = re.search(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", url)
        url_string = url_match.group(0) if url_match else None

        if not url_string:
            return "Sorry, I couldn't find a URL in that message."

        # If a URL was found, remove it from the string to get the trailing text
        if url_string:
            url_string = url_string.strip('<>')
            trailing_text = url.replace(url_string, '').strip()
            if trailing_text:
                prompt = trailing_text
        if url_string.endswith('.pdf'):
            page_text = get_text_from_pdf(url_string)
        else:
            my_config = deepcopy(DEFAULT_CONFIG)
            my_config['DEFAULT']['user_agent'] = request_headers['User-Agent']
            downloaded = fetch_url(url_string, config=my_config)
            if downloaded is None:
                return f"Sorry, I couldn't download content from the URL {url_string}."
            page_text = extract(downloaded)

    return page_text
