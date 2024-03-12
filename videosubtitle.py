import time
import re
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator

def get_video_id(url):
    try:
        video_id_match = re.search(r"(?<=v=)([a-zA-Z0-9_-]+)", url)
        if video_id_match:
            video_id = video_id_match.group(1)
            return video_id
        else:
            print("Video ID not found in the URL.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None




def translate_subtitles(url, target_language='ta'):
    try:
        # Get video ID
        video_id = get_video_id(url)

        if video_id:
            # Get video transcripts
            transcripts = YouTubeTranscriptApi.get_transcript(video_id)
            translator = Translator()

            translated_subtitles = []

            for segment in transcripts:
                original_text = segment['text']
                translated_text = translator.translate(original_text, dest=target_language).text

                translated_subtitles.append({
                    'start': segment['start'],
                    'end': segment['start'] + segment['duration'],
                    'text': translated_text
                })

            return translated_subtitles

        else:
            print("Failed to retrieve the video ID. Check the URL or try again later.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=4NmuR-O1LOE&t=905s"
    target_language = "ta"  # Change to the desired language code

    translated_subtitles = translate_subtitles(video_url, target_language)

    if translated_subtitles:
        # Display the translated subtitles
        for segment in translated_subtitles:
            print(f'Start: {segment["start"]}, End: {segment["end"]}')
            print(f'Translated: {segment["text"]}')
            print('-' * 50)
    else:
        print("Subtitle translation failed. Please check the URL or try again later.")
