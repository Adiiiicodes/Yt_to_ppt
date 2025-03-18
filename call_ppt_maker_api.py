import os
import requests
import json

# PPTMaker API credentials
# Replace this value with your valid PPTMaker API token.
PPT_API_TOKEN = "3291da4e-9761-4a56-9464-0df6c15e93a8"
# Use the provided token as the bearer token
BEARER_TOKEN = PPT_API_TOKEN

def call_pptmaker_api(payload):
    """
    Calls the PPTMaker API using the provided JSON payload and a PPTX template file.
    On success, saves the generated PPTX file and returns its filename.
    
    The API requires:
      - A multipart/form-data request
      - A 'files' field containing the template PPTX file.
      - A 'jsonData' field (as text) containing the JSON payload.
      - An 'Authorization' header in the format: "Bearer <token>"
    """
    url = "https://gen.powerpointgeneratorapi.com/v1.0/generator/create"
    template_file = "slides_as_template.pptx"  # Ensure this file exists in your project folder

    if not os.path.exists(template_file):
        print(f"Template file '{template_file}' not found.")
        return None

    try:
        with open(template_file, "rb") as f:
            files = {
                "files": (
                    template_file,
                    f,
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
            }
            data = {
                "jsonData": json.dumps(payload)
            }
            headers = {
                "Authorization": f"Bearer {BEARER_TOKEN}"
            }
            print("Sending payload to PPTMaker API...")
            response = requests.post(url, data=data, files=files, headers=headers, timeout=360)
            print("Response status code:", response.status_code)
            print("Response content:", response.content)

            if response.status_code == 200:
                try:
                    output_filename = "generated_presentation.pptx"
                    with open(output_filename, "wb") as out_file:
                        out_file.write(response.content)
                    print("PPT generated successfully!")
                    return output_filename
                except Exception as inner_e:
                    print("Exception while writing PPT file:", inner_e)
                    return None
            else:
                print("Error in PPTMaker API:", response.text)
                return None
    except Exception as e:
        print("Exception in call_pptmaker_api:", e)
        return None
