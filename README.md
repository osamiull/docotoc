# docotoc

# Medical Transcription and Email Generation

This project transcribes medical audio files, corrects spelling, and generates concise emails based on the transcriptions using OpenAI's GPT-4 model.

## Problem Statement

In today's healthcare landscape, both patients and healthcare providers are heavily reliant on Electronic Health Records (EHRs) for effective care. However, interacting with EHRs presents significant challenges:

- The American Medical Association has identified the complexity and confusion associated with using apps for patient-doctor communication and health record access as the primary barrier for patients to adopt digital health.
- The American College of Family Physicians estimates that a doctor must make 1 million clicks a year to complete their tasks.
- The current approach of a graphical user interface (GUI) has failed both physicians and patients by causing confusion, frustration, information overload, burnout, and errors.

We are pioneering the use of AI agents to intelligently determine the user's intention, interactively explain the choices, correct any AI-made errors, and then allow humans to make the final decisions.

In our proof-of-concept build, we focus on a single use case of patients asking questions to their doctors by email. In the current EPIC MyChart app, it takes 9 steps for this task. We design an AI agent to simplify this process into one click.

### Our Approach

Our AI agent streamlines the workflow with the following key features:

1. Determine the Intention: Intelligently identify the user's intention from their input.
2. Offer Explanation: Interactively explain its reasoning and thought process to the user.
3. Seek Confirmation: Request user confirmation before taking any actions.

### How We Build It

- Voice to Text: Convert spoken words into written text.
- Question Embedding: Process and understand the patient's question.
- Communication Embedding: Incorporate context from previous doctor-patient communications.
- Question-Answering: Provide immediate answers if they exist in previous communications.
- Doctor Matching: Identify the most suitable doctor for unanswered questions.
- AI-Generated Draft: Use generative AI to draft an email to the doctor.

## Prerequisites

- Docker
- Docker Compose
- OpenAI API key

## Setup

1. Clone the repository:
git clone <repository-url>
cd <repository-directory>

2. Create a `.env` file in the root directory with your OpenAI API key:

OPENAI_API_KEY=your_api_key_here


3. Place your audio files in the `audio_files` directory. The supported files are:
- 0_Blood Sugar Monitoring Guidelines.mp3
- 1_Calcium Supplements_ Stay or Go_.mp3
- 2_Managing Daily Tasks with Alzheimer's.mp3
- 3_Can I Stop My Hypertension Meds_.mp3
- 4_Asthma Meds in Pregnancy_ Safety Guide.mp3
- 5_Metformin and Constipation Concerns.mp3
- 6_New Options for Depression Treatment.mp3
- 7_Breast Cancer Gene Inheritance Risks.mp3
- 8_Monitoring Your Heart Health.mp3
- 9_Managing Arthritis and Exercise Pain.mp3

## Running the Application

From the root directory of the repository, run the following command:
docker compose build && docker compose run --rm app


This command will:
1. Build the Docker image for the application
2. Start the Docker container

The application will process generate an email based on the content from the input from the patient.

## Viewing Results

The application will output the results to the console, including:
- Generated email

Each file's results will be separated by a line of dashes for easy reading.

## Stopping the Application

To stop the application, use Ctrl+C in the terminal where it's running, or open another terminal and run:
docker-compose down


## Troubleshooting

If you encounter any issues:
1. Ensure your `.env` file is correctly set up with your OpenAI API key.
2. Check that your audio files are in the correct directory and have the exact names listed above.
3. Make sure you have sufficient credits on your OpenAI account.
4. If you encounter rate limiting issues, you may need to adjust the retry logic in the code.

For any persistent issues, please refer to the error messages in the console output or check the Docker logs:
docker-compose logs


## Future Expansion

- Incorporate More Agents: Add medication agents, scheduling agents, and others to enhance system capabilities.
- Expand to the Doctor Space: Extend our work to address physician frustrations with point-and-click GUIs.


See the company website and the slide by Dr. Simon Linwood for his future plan(s). 
https://www.canva.com/design/DAGNbcUskx4/vM5CihqUfnARc3k81M1VNw/edit
