from google.cloud import aiplatform
from google.cloud import speech_v1
import yt_dlp
import os
import tempfile
import time

def download_youtube_audio(url, output_path=None):
    """
    Download audio from YouTube URL using yt-dlp
    """
    try:
        print(f"Attempting to download audio from: {url}")
        
        if output_path is None:
            output_path = tempfile.mktemp(suffix='.mp4')
            
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_path,
            'quiet': False,
        }
        
        print("Downloading audio stream...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            print(f"Title: {info.get('title', 'Unknown')}")
            print(f"Duration: {info.get('duration', 0)} seconds")
            
            # Download the audio
            ydl.download([url])
            
        print(f"Successfully downloaded audio to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading YouTube audio: {str(e)}")
        print("Full error details:", e.__class__.__name__)
        return None

def transcribe_audio(audio_path, project_id):
    """
    Transcribe audio using Google Cloud Speech-to-Text
    """
    try:
        print("Initializing Speech-to-Text client...")
        client = speech_v1.SpeechClient()
        
        # Read audio file
        print(f"Reading audio file: {audio_path}")
        with open(audio_path, 'rb') as audio_file:
            content = audio_file.read()
            
        print("Starting transcription...")
        audio = speech_v1.RecognitionAudio(content=content)
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            audio_channel_count=1,
            enable_word_time_offsets=True
        )
        
        # Perform the transcription
        response = client.recognize(config=config, audio=audio)
        
        # Combine all transcriptions
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + "\n"
            
        print("Transcription completed successfully")
        return transcript
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        print("Full error details:", e.__class__.__name__)
        return None

def process_youtube_video(url, project_id):
    """
    Main function to process YouTube video and get transcript
    """
    # Create temporary directory for audio file
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, 'audio.mp3')
    
    try:
        # Download audio
        print("Starting YouTube video processing...")
        downloaded_path = download_youtube_audio(url, audio_path)
        
        if not downloaded_path:
            print("Failed to download audio")
            return None
            
        # Transcribe audio
        transcript = transcribe_audio(downloaded_path, project_id)
        
        if transcript:
            print("\nTranscript:")
            print(transcript)
            return transcript
        else:
            print("Failed to generate transcript")
            return None
            
    finally:
        # Cleanup
        try:
            if os.path.exists(audio_path):
                os.remove(audio_path)
            os.rmdir(temp_dir)
        except Exception as e:
            print(f"Warning: Cleanup failed: {str(e)}")

def main():
    # Your Google Cloud project ID
    PROJECT_ID = "astute-sky-332601"
    
    # The specific YouTube URL
    youtube_url = "https://www.youtube.com/watch?v=bc7170FZK3s"
    
    print(f"Processing YouTube video: {youtube_url}")
    transcript = process_youtube_video(youtube_url, PROJECT_ID)
    
    if transcript:
        # Save transcript to file
        output_file = "transcript.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"\nTranscript saved to {output_file}")
    else:
        print("Failed to process the video")

if __name__ == "__main__":
    main() 