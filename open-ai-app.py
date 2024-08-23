import os
import time
import json
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

# def generate_email(client, corrected_text, max_retries=3):
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

# def handle_patient_interaction(client, user_input, max_retries=3):
    system_prompt = """
    You are a helpful assistant talking to a patient. You will start with "Welcome to DocoToc. How may I help you today?". Then wait for the answers. The person you are talking to is a patient. Please ask clarifying questions as necessary.  

    Right now, you can only handle a single task to help your patient to ask a question to their doctor. And you can help the patient to choose the right doctor, and then draft an email for them. 

    You will not handle medication refills. You will not handle scheduling. You will not handle bill payment. 

    If the user asks something that is out of your knowledge or capabilities, politely inform them that you are a POC prototype and unable to assist with their request yet. Please also tell your patient what you can do so far. And ask for anything else you can be of help. If there is an exception or error, handle it gracefully and provide a useful response.

    If you find out the patient's ask is about asking a question to their doctor, then, confirm "so you want me to help you asking this question to your doctor?". As soon as you get a positive confirmation, just output a JSON file showing the patient's question. Then you can stop. Please do not say anything else.
    """

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content.strip()
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Exponential backoff
            else:
                logger.error("Max retries reached. Unable to handle patient interaction.")
                raise e

# def handle_patient_interaction(client, user_input, max_retries=3):
    system_prompt = """
    You are a helpful assistant talking to a patient. You will start with "Welcome to DocoToc. How may I help you today?". Then wait for the answers. The person you are talking to is a patient. Please ask clarifying questions as necessary.  

    Right now, you can only handle a single task to help your patient to ask a question to their doctor. And you can help the patient to choose the right doctor, and then draft an email for them. 

    You will not handle medication refills. You will not handle scheduling. You will not handle bill payment. 

    If the user asks something that is out of your knowledge or capabilities, politely inform them that you are a POC prototype and unable to assist with their request yet. Please also tell your patient what you can do so far. And ask for anything else you can be of help. If there is an exception or error, handle it gracefully and provide a useful response.

    If you find out the patient's ask is about asking a question to their doctor, then, confirm "so you want me to help you asking this question to your doctor?". As soon as you get a positive confirmation, just output a JSON file showing the patient's question. Then you can stop. Please do not say anything else.
    """

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content.strip()
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Exponential backoff
            else:
                logger.error("Max retries reached. Unable to handle patient interaction.")
                raise e

# def handle_patient_interaction(client, user_input, conversation_history, max_retries=3):
    system_prompt = """
    You are a helpful assistant talking to a patient. You will start with "Welcome to DocoToc. How may I help you today?". Then wait for the answers. The person you are talking to is a patient. Please ask clarifying questions as necessary.  

    Right now, you can only handle a single task to help your patient to ask a question to their doctor. And you can help the patient to choose the right doctor, and then draft an email for them. 

    You will not handle medication refills. You will not handle scheduling. You will not handle bill payment. 

    If the user asks something that is out of your knowledge or capabilities, politely inform them that you are a POC prototype and unable to assist with their request yet. Please also tell your patient what you can do so far. And ask for anything else you can be of help. If there is an exception or error, handle it gracefully and provide a useful response.

    If you find out the patient's ask is about asking a question to their doctor, then, confirm "so you want me to help you asking this question to your doctor?". As soon as you get a positive confirmation, respond with a JSON object containing the patient's question. The JSON should be in the format: {"patient_question": "The patient's question here"}. Do not say anything else after outputting the JSON.
    """

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *conversation_history,
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content.strip()
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Exponential backoff
            else:
                logger.error("Max retries reached. Unable to handle patient interaction.")
                raise e

# def handle_patient_interaction(client, user_input, conversation_history, max_retries=3):
    system_prompt = """
    You are a helpful assistant talking to a patient. You will start with "Welcome to DocoToc. How may I help you today?". Then wait for the answers. The person you are talking to is a patient. Please ask clarifying questions as necessary.  

    Right now, you can only handle a single task to help your patient to ask a question to their doctor. And you can help the patient to choose the right doctor, and then draft an email for them. 

    You will not handle medication refills. You will not handle scheduling. You will not handle bill payment. 

    If the user asks something that is out of your knowledge or capabilities, politely inform them that you are a POC prototype and unable to assist with their request yet. Please also tell your patient what you can do so far. And ask for anything else you can be of help. If there is an exception or error, handle it gracefully and provide a useful response.

    If you find out the patient's ask is about asking a question to their doctor, then, confirm "so you want me to help you asking this question to your doctor?". As soon as you get a positive confirmation, respond with a JSON object containing the patient's question and the doctor's name. The JSON should be in the format: {"patient_question": "The patient's question here", "doctor_name": "Dr. Name"}. Do not say anything else after outputting the JSON.
    """

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *conversation_history,
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content.strip()
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Exponential backoff
            else:
                logger.error("Max retries reached. Unable to handle patient interaction.")
                raise e

# def generate_email(client, patient_question, doctor_name, max_retries=3):
    prompt = f"""
    Please draft an email to {doctor_name} regarding the following question:
    
    Dear {doctor_name},

    {patient_question}

    Thank you,
    [Your Name]
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

# def handle_patient_interaction(client, user_input, conversation_history, max_retries=3):
    system_prompt = """
    You are a helpful assistant talking to a patient. You will start with "Welcome to DocoToc. How may I help you today?". Then wait for the answers. The person you are talking to is a patient. Please ask clarifying questions as necessary.  

    Right now, you can only handle a single task to help your patient to ask a question to their doctor. And you can help the patient to choose the right doctor, and then draft an email for them. 

    You will not handle medication refills. You will not handle scheduling. You will not handle bill payment. 

    If the user asks something that is out of your knowledge or capabilities, politely inform them that you are a POC prototype and unable to assist with their request yet. Please also tell your patient what you can do so far. And ask for anything else you can be of help. If there is an exception or error, handle it gracefully and provide a useful response.

    If you find out the patient's ask is about asking a question to their doctor, then, confirm "so you want me to help you asking this question to your doctor?". As soon as you get a positive confirmation, respond with a JSON object containing the patient's question and the doctor's name. The JSON should be in the format: {"patient_question": "The patient's question here", "doctor_name": "Dr. Name"}. Do not say anything else after outputting the JSON.
    """

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *conversation_history,
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content.strip()
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Exponential backoff
            else:
                logger.error("Max retries reached. Unable to handle patient interaction.")
                raise e

def generate_email(client, patient_question, doctor_name, patient_name, max_retries=3):
    prompt = f"""
    Please draft an email to {doctor_name} regarding the following question:
    
    Dear {doctor_name},

    {patient_question}

    Sincerely,
    {patient_name}
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


def handle_patient_interaction(client, user_input, conversation_history, max_retries=3):
    system_prompt = """
    You are a helpful assistant talking to a patient. You will start with "Welcome to DocoToc. How may I help you today?". Then wait for the answers. The person you are talking to is a patient. Please ask clarifying questions as necessary.  

    Right now, you can only handle a single task to help your patient to ask a question to their doctor. And you can help the patient to choose the right doctor, and then draft an email for them. 

    You will not handle medication refills. You will not handle scheduling. You will not handle bill payment. 

    If the user asks something that is out of your knowledge or capabilities, politely inform them that you are a POC prototype and unable to assist with their request yet. Please also tell your patient what you can do so far. And ask for anything else you can be of help. If there is an exception or error, handle it gracefully and provide a useful response.

    If you find out the patient's ask is about asking a question to their doctor, then, confirm "so you want me to help you asking this question to your doctor?". As soon as you get a positive confirmation, respond with a JSON object containing the patient's question and the doctor's name. The JSON should be in the format: {"patient_question": "The patient's question here", "doctor_name": "Dr. Name", "patient_name": "Patient Name"}. Do not say anything else after outputting the JSON.
    """

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *conversation_history,
                    {"role": "user", "content": user_input}
                ]
            )
            return response.choices[0].message.content.strip()
        except RateLimitError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Exponential backoff
            else:
                logger.error("Max retries reached. Unable to handle patient interaction.")
                raise e

# def main():
#     try:
#         api_key = get_api_key()
#         logger.info(f"API Key: {api_key[:5]}...{api_key[-5:]}")  # Log first and last 5 characters
        
#         client = OpenAI(api_key=api_key)
        
#         audio_files = [
#             "0_Blood Sugar Monitoring Guidelines.mp3",
#             "1_Calcium Supplements_ Stay or Go_.mp3",
#             "2_Managing Daily Tasks with Alzheimer's.mp3",
#             "3_Can I Stop My Hypertension Meds_.mp3",
#             "4_Asthma Meds in Pregnancy_ Safety Guide.mp3",
#             "5_Metformin and Constipation Concerns.mp3",
#             "6_New Options for Depression Treatment.mp3",
#             "7_Breast Cancer Gene Inheritance Risks.mp3",
#             "8_Monitoring Your Heart Health.mp3",
#             "9_Managing Arthritis and Exercise Pain.mp3"
#         ]
        
#         for audio_file in audio_files:
#             # print("Current working directory:", os.getcwd())
#             # print("Contents of audio_files directory:", os.listdir("audio_files"))
#             logger.info(f"Processing file: {audio_file}")
            
#             # Transcribe audio
#             audio_file_path = os.path.join("audio_files", audio_file)
#             transcription = transcribe_with_retry(client, audio_file_path)
#             logger.info("Transcription completed")
            
#             # Correct spelling
#             corrected_text = correct_spelling(client, transcription)
#             logger.info("Spelling correction completed")
            
#             # Generate email
#             email_content = generate_email(client, corrected_text)
#             logger.info("Email generation completed")
            
#             # Print results
#             print(f"\nFile: {audio_file}")
#             print("Original Transcription:")
#             print(transcription)
#             print("\nCorrected Transcription:")
#             print(corrected_text)
#             print("\nGenerated Email:")
#             print(email_content)
#             print("-" * 50)
        
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")

def main():
    try:
        api_key = get_api_key()
        logger.info(f"API Key: {api_key[:5]}...{api_key[-5:]}")  # Log first and last 5 characters
        
        client = OpenAI(api_key=api_key)
        
        # Handle patient interaction
        print("Welcome to DocoToc. How may I help you today?")
        conversation_history = []
        patient_name = input("Please enter your name: ")  # Ask for the patient's name

        while True:
            try:
                user_input = input("Patient: ")
                if user_input.lower() == 'exit':
                    break
                
                conversation_history.append({"role": "user", "content": user_input})
                response = handle_patient_interaction(client, user_input, conversation_history)
                print("DocoToc:", response)
                conversation_history.append({"role": "assistant", "content": response})
                
                # Check if the response is a JSON object containing a patient question
                try:
                    question_json = json.loads(response)
                    if 'patient_question' in question_json and 'doctor_name' in question_json:
                        print(f"Patient question for {question_json['doctor_name']} detected. Generating email...")
                        email_content = generate_email(client, question_json['patient_question'], question_json['doctor_name'], patient_name)
                        print(f"\nGenerated Email for {question_json['doctor_name']}:")
                        print(email_content)
                        break
                except json.JSONDecodeError:
                    pass  # Not a JSON response, continue the conversation
            except EOFError:
                print("No input received. Exiting.")
                break
        
        # audio_files = [
        #     "0_Blood Sugar Monitoring Guidelines.mp3",
        #     "1_Calcium Supplements_ Stay or Go_.mp3",
        #     "2_Managing Daily Tasks with Alzheimer's.mp3",
        #     "3_Can I Stop My Hypertension Meds_.mp3",
        #     "4_Asthma Meds in Pregnancy_ Safety Guide.mp3",
        #     "5_Metformin and Constipation Concerns.mp3",
        #     "6_New Options for Depression Treatment.mp3",
        #     "7_Breast Cancer Gene Inheritance Risks.mp3",
        #     "8_Monitoring Your Heart Health.mp3",
        #     "9_Managing Arthritis and Exercise Pain.mp3"
        # ]
        
        # for audio_file in audio_files:
            # logger.info(f"Processing file: {audio_file}")
            
            # Transcribe audio
            # audio_file_path = os.path.join("audio_files", audio_file)
            # transcription = transcribe_with_retry(client, audio_file_path)
            # logger.info("Transcription completed")
            
            # Correct spelling
            # corrected_text = correct_spelling(client, transcription)
            # logger.info("Spelling correction completed")
            
            # Generate email
            # email_content = generate_email(client, corrected_text)
            # logger.info("Email generation completed")
            
            # Print results
            # print(f"\nFile: {audio_file}")
            # print("Original Transcription:")
            # print(transcription)
            # print("\nCorrected Transcription:")
            # print(corrected_text)
            # print("\nGenerated Email:")
            # print(email_content)
            # print("-" * 50)
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     main()