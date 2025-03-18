import requests
import json

def generate_ppt_payload(transcription):
    """
    Converts the transcription text into a JSON payload in the format expected by the PPTMaker API.
    This function calls the Groq API using function calling. It instructs the API to use the transcription
    to generate a JSON payload with a top-level "presentation" key containing:
      - template: "slides_as_template.pptx"
      - export_version: "Pptx2010"
      - slides: an array of slide objects, each with a "type" ("slide"), a zero-based "slide_index",
        and a "shapes" array containing objects with "name" and "content".
    """
    groq_api_url = "https://api.groq.com/openai/v1/chat/completions"  # Replace with your actual endpoint
    groq_api_token = "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"  # Replace with your token

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {groq_api_token}"
    }
    
    data = {
        "model": "llama3-70b-8192",  # Add the model parameter as required by the API.
        "messages": [
            {
                "role": "system",
                "content": (
                    "You aree an assistant that converts a YouTube video transcription into a JSON payload for the PPTMaker API. "
                    "The PPTMaker API expects a JSON object with a 'presentation' key. The 'presentation' object must contain: "
                    "'template' (set to 'slides_as_template.pptx'), 'export_version' (set to 'Pptx2010'), and 'slides'. "
                    "The 'slides' key should be an array of slide objects. Each slide object must include 'type' (which should be 'slide'), "
                    "'slide_index' (a zero-based index), and 'shapes' (an array of shape objects). Each shape object should have a 'name' and a 'content'. "
                    "For example, the title slide (slide_index 0) should have a shape with the name 'Title 1' whose content is the first sentence of the transcription. "
                    "Subsequent slides should use subsequent parts of the transcription and use shape names like 'Content 1', 'Content 2', etc. "
                    "Ensure that the JSON is valid and exactly follows this structure."
                )
            },
            {
                "role": "user",
                "content": transcription
            }
        ],
        "functions": [
            {
                "name": "generate_ppt_payload",
                "description": "Generate a PPTMaker payload from a YouTube video transcription.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "presentation": {
                            "type": "object",
                            "properties": {
                                "template": {
                                    "type": "string",
                                    "description": "PPTX template file name."
                                },
                                "export_version": {
                                    "type": "string",
                                    "description": "Export version identifier."
                                },
                                "slides": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "type": {
                                                "type": "string",
                                                "description": "Slide type, always 'slide'."
                                            },
                                            "slide_index": {
                                                "type": "number",
                                                "description": "Zero-based index of the slide."
                                            },
                                            "shapes": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "name": {
                                                            "type": "string",
                                                            "description": "The shape name."
                                                        },
                                                        "content": {
                                                            "type": "string",
                                                            "description": "The content to place in the shape."
                                                        }
                                                    },
                                                    "required": ["name", "content"]
                                                }
                                            }
                                        },
                                        "required": ["type", "slide_index", "shapes"]
                                    }
                                }
                            },
                            "required": ["template", "export_version", "slides"]
                        }
                    },
                    "required": ["presentation"]
                }
            }
        ],
        "function_call": {"name": "generate_ppt_payload"}
    }
    
    response = requests.post(groq_api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_data = response.json()
        try:
            # Extract the generated arguments from the function call response.
            function_call = response_data["choices"][0]["message"]["function_call"]
            arguments_str = function_call["arguments"]
            payload = json.loads(arguments_str)
            return payload
        except Exception as e:
            raise Exception("Failed to parse Groq API response: " + str(e))
    else:
        error_message = f"Groq API returned an error ({response.status_code}): {response.text}"
        raise Exception(error_message)
