# Generate text to speech
import logging
import boto3
from services.supabase_service import supabase_service
from datetime import datetime

logger = logging.getLogger(__name__)

polly = boto3.client('polly')


def generate_tts(text_input: str, language_code: str):
    """
    Generates audio overview.

    Args:
    text_input : script
    language_code : en-IN or hi-IN
    """

    try:
        response = polly.synthesize_speech(
            Engine='neural',
            Text=text_input,
            # TextType='ssml',
            LanguageCode=language_code,  # 'hi-IN'
            OutputFormat='mp3',
            VoiceId='Kajal'
        )

        audio_data = response['AudioStream'].read()

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_{timestamp}.mp3"

        # Upload to Supabase storage
        upload_response = supabase_service.upload_file(
            file_path=filename,
            file_data=audio_data
        )

        # Get public URL
        public_url = supabase_service.get_public_url(filename)

        logger.info(f"TTS audio uploaded successfully: {filename}")

        return {
            "success": True,
            "filename": filename,
            "public_url": public_url,
            "upload_response": upload_response
        }

    except Exception as e:
        logger.error(f"Error generating TTS: {str(e)}")
        raise e
