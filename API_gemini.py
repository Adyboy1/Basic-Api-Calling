import google.generativeai as genai
import os
import json
import time

# Get and check API key from environment variable
api_key = os.environ.get("API_KEY")
if not api_key:
    print("[ERROR] API_KEY environment variable not set.")
    exit(1)

# Configure the Gemini API
genai.configure(api_key=api_key)

# Load the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Read prompts from the input file
input_file_path = 'input.txt'
try:
    with open(input_file_path, "r") as infile:
        prompts = infile.readlines()
except FileNotFoundError:
    print(f"[ERROR] Could not find {input_file_path}")
    exit(1)

# Store results here
output_data = []

# Function to get response from Gemini API
def get_gemini_response(prompt):
    start_time = time.time()
    try:
        response = model.generate_content(prompt.strip())
        end_time = time.time()
        message = response.text
    except Exception as e:
        end_time = time.time()
        message = f"[ERROR] API call failed: {e}"
        print(message)

    return {
        "Prompt": prompt.strip(),
        "Message": message,
        "TimeSent": int(start_time),
        "TimeRecvd": int(end_time),
        "Source": "Gemini"
    }

# Process each prompt
for prompt in prompts:
    if prompt.strip():  # skip empty lines
        print(f"\n[INFO] Sending prompt: {prompt.strip()}")
        result = get_gemini_response(prompt)
        print(f"[INFO] Received response: {result['Message'][:100]}...")  # Print a preview
        output_data.append(result)

# Save the output to a JSON file
output_file_path = 'output.json'
with open(output_file_path, "w") as outfile:
    json.dump(output_data, outfile, indent=4)

print(f"\n✅ All responses saved to {output_file_path}")
