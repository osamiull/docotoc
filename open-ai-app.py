import os
import time
from dotenv import load_dotenv
import logging
from openai import OpenAI, RateLimitError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

def get_api_key():
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key

def transcribe_with_retry(client, file_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            with open(file_path, "rb") as audio_file:
                return client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Exponential backoff
            else:
                logger.error("Max retries reached. Unable to transcribe.")
                raise e

def correct_spelling(client, transcription, max_retries=3):
    system_prompt = """
    You are a helpful assistant specializing in medical terminology. 
    Your task is to correct any spelling discrepancies in the transcribed text about blood sugar checks. 
    Make sure that medical terms and procedures are spelled correctly. 
    Only add necessary punctuation such as periods, commas, and capitalization, and use only the context provided.
    """

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcription}
                ]
            )
            return response.choices[0].message.content
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Exponential backoff
            else:
                logger.error("Max retries reached. Unable to correct spelling.")
                raise e

def main():
    try:
        api_key = get_api_key()
        logger.info(f"API Key: {api_key[:5]}...{api_key[-5:]}")  # Log first and last 5 characters
        
        client = OpenAI(api_key=api_key)
        
        # Transcribe audio
        audio_file_path = "Blood Sugar Check Questions.mp3"
        transcription = transcribe_with_retry(client, audio_file_path)
        logger.info("Transcription completed")
        
        # Correct spelling
        corrected_text = correct_spelling(client, transcription)
        logger.info("Spelling correction completed")
        
        # Print results
        print("Original Transcription:")
        print(transcription)
        print("\nCorrected Transcription:")
        print(corrected_text)
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()