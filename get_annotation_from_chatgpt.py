import requests
import json
import matplotlib.pyplot as plt

# Replace 'YOUR_API_KEY' with your API key (you already guessed it, right?)
api_key = 'YOUR_API_KEY'
api_url = 'https://api.openai.com/v1/chat/completions'

# Converting into json
data_json = dataset.to_json(orient='records')

# Definuing the prompt
prompt = (
    f"Here is the data in JSON format: {data_json}. "
    "Please provide a detailed analysis of the data in 800 characters. "
    "Shorten values in the most efficient and meaningful way possible. Every number shall have a maximum of three digits. "
    "Always provide the corresponding percentage value for deviations. "
    "Please provide the top 5 most notable insights from the data, ranked by importance. "
    "Include insights on trends, mention any extreme values, and provide any other interesting observations. "
    "Ensure the description is valuable and insightful and in german language."
    "Do not use a main heading or a summary. "
)

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

payload = {
    'model': 'gpt-4-turbo',
    'messages': [
        {'role': 'system', 'content': 'You are a controller and data scientist.'},
        {'role': 'user', 'content': prompt}
    ],
    'max_tokens': 1000,
    'temperature': 0.7
}

response = requests.post(api_url, headers=headers, json=payload)

# Check, if response is ok
if response.status_code == 200:
    response_data = response.json()
    description = response_data['choices'][0]['message']['content']
else:
    description = f"Fehler: {response.status_code}\n{response.text}"

# Split the description into lines and format for plotting
formatted_text = ""
lines = description.split('\n')

for line in lines:
    # Delete '**' and add a linefeed after ':'
    line = line.replace('**', '')
    if ':' in line:
        parts = line.split(':', 1)
        if len(parts) == 2:
            formatted_text += f"{parts[0].strip()}: \n{parts[1].strip()}\n"
        else:
            formatted_text += f"{line.strip()}\n"
    else:
        formatted_text += f"{line.strip()}\n"

# Plotting of description
plt.figure(figsize=(10, 6))
plt.text(0.01, 0.99, formatted_text, ha='left', va='top', wrap=True, fontsize=12)
plt.axis('off')
plt.show()