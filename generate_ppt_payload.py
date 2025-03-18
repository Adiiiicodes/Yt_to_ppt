import requests
import json

# Groq API Credentials
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Groq API endpoint
GROQ_API_TOKEN = "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"  # Groq API token

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GROQ_API_TOKEN}"
}

def generate_ppt_content(transcription):
    """
    This function calls the Groq API using the transcription text and generates content for PowerPoint slides.
    It requests the content to be split into two points per slide, each point being 70 words.
    """
    data = {
        "model": "llama3-70b-8192",  # Add the model parameter as required by the API.
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an assistant that converts a transcription into structured summarized content for a PowerPoint presentation. "
                    "The transcription content is going to be split into slides with exactly two bullet points per slide. "
                    
                    "Generate a summary of the transcription where, after every 70 words, the sentence should end and a new sentence should start. "
                    "This is important as each point will be a separate bullet point on a slide(you just have to give me a paragraph of the summary) "
                    "There should be no '{' or '}' at the beginning and end of the response you provide."
                )
            },
            {
                "role": "user",
                "content": transcription
            }
        ],
        "functions": [
            {
                "name": "generate_ppt_content",
                "description": "Generate content for PowerPoint presentation based on transcription, split into two points of 70 words each per slide.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ppt_content": {
                            "type": "string",
                            "description": "The content for the slides, divided into two bullet points per slide, each with 70 words."
                        }
                    },
                    "required": ["ppt_content"]
                }
            }
        ],
        "function_call": {"name": "generate_ppt_content"}
    }

    # Make request to Groq API to generate the PowerPoint content
    response = requests.post(GROQ_API_URL, headers=HEADERS, json=data)

    if response.status_code == 200:
        response_data = response.json()
        try:
            # Extract the generated content for PowerPoint slides
            function_call = response_data["choices"][0]["message"]["function_call"]
            ppt_content = function_call["arguments"]  # The content for the PowerPoint slides

            print("✅ Generated PowerPoint Content:\n", ppt_content)

            return ppt_content
        except Exception as e:
            raise Exception("❌ Failed to parse Groq API response: " + str(e))
    else:
        error_message = f"⚠️ Groq API returned an error ({response.status_code}): {response.text}"
        raise Exception(error_message)
