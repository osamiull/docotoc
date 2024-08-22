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

def generate_email(client, corrected_text, max_retries=3):
    prompt = f"""
    Please use the following question to generate an email to my doctor. 
    Please limit the message to 450 characters:

    {corrected_text}
    """

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes concise emails."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150  # Approximately 450 characters
            )
            return response.choices[0].message.content.strip()
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Exponential backoff
            else:
                logger.error("Max retries reached. Unable to generate email.")
                raise e

def main():
    try:
        api_key = get_api_key()
        logger.info(f"API Key: {api_key[:5]}...{api_key[-5:]}")  # Log first and last 5 characters
        
        client = OpenAI(api_key=api_key)
        
        audio_files = [
            "0_Blood Sugar Monitoring Guidelines.mp3",
            "1_Calcium Supplements_ Stay or Go_.mp3",
            "2_Managing Daily Tasks with Alzheimer's.mp3",
            "3_Can I Stop My Hypertension Meds_.mp3",
            "4_Asthma Meds in Pregnancy_ Safety Guide.mp3",
            "5_Metformin and Constipation Concerns.mp3",
            "6_New Options for Depression Treatment.mp3",
            "7_Breast Cancer Gene Inheritance Risks.mp3",
            "8_Monitoring Your Heart Health.mp3",
            "9_Managing Arthritis and Exercise Pain.mp3"
        ]
        
        for audio_file in audio_files:
            # print("Current working directory:", os.getcwd())
            # print("Contents of audio_files directory:", os.listdir("audio_files"))
            logger.info(f"Processing file: {audio_file}")
            
            # Transcribe audio
            audio_file_path = os.path.join("audio_files", audio_file)
            transcription = transcribe_with_retry(client, audio_file_path)
            logger.info("Transcription completed")
            
            # Correct spelling
            corrected_text = correct_spelling(client, transcription)
            logger.info("Spelling correction completed")
            
            # Generate email
            email_content = generate_email(client, corrected_text)
            logger.info("Email generation completed")
            
            # Print results
            print(f"\nFile: {audio_file}")
            print("Original Transcription:")
            print(transcription)
            print("\nCorrected Transcription:")
            print(corrected_text)
            print("\nGenerated Email:")
            print(email_content)
            print("-" * 50)
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
