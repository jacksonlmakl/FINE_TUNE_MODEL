import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os
import json
from openai import OpenAI

keys = json.load(open("keys.json"))
os.environ["OPENAI_API_KEY"] = keys['openai']
def get_all_files():

    # Define the directory path
    directory = "train/"

    # Initialize an empty list to store the results
    x = []

    # Iterate over all JSON files in the directory
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith(".json"):
            # Load the JSON file as a dictionary
            with open(os.path.join(directory, filename), "r") as file:
                data = json.load(file)

            # Extract the embeddings from the dictionary and create a new dictionary
            embeddings_data = {"file_name": filename, "embeddings": data["embeddings"]}

            # Append the new dictionary to the list
            x.append(embeddings_data)
    return x


def find_most_similar(target):
    library = get_all_files()
    # Convert 'target' to a numpy array
    target_array = np.array(target)

    # Initialize variables to keep track of the most similar embeddings and their similarity scores
    most_similar_file_names = []
    max_similarity_score = -1  # Initialize to a negative value as similarity scores are between -1 and 1

    # Iterate over each item in the library
    for item in library:
        # Calculate cosine similarity between 'target' and the embeddings in 'item'
        similarities = cosine_similarity(target_array.reshape(1, -1), np.array(item['embeddings']).reshape(1, -1))

        # Check if the similarity score is higher than the current maximum
        if similarities[0][0] > max_similarity_score:
            # Update the maximum similarity score and the most similar embeddings' file names
            max_similarity_score = similarities[0][0]
            most_similar_file_names.append(item['file_name'])
        # If the similarity score is equal to the current maximum, append the file name to the list
        elif similarities[0][0] == max_similarity_score:
            most_similar_file_names.append(item['file_name'])

    return most_similar_file_names

# Usage

def similarity(text):
    client = OpenAI()
    embedding_response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    target_embeddings = embedding_response.data[0].embedding

    most_similar_embeddings = find_most_similar(target_embeddings)
    print("Most similar embeddings:", most_similar_embeddings)
    return most_similar_embeddings

def combine_training_data(file_names):
    combined_data = {'training': []}

    # Iterate through each file name
    for file_name in file_names:
        with open(f'train/{file_name}', 'r') as file:
            data = json.load(file)
            # Extract the training data from the loaded JSON
            training_data = data.get('training', [])
            # Extend the combined data list with the training data from the current file
            combined_data['training'].extend(training_data)

    return combined_data

def upload_training_data(combined_training_data):
    client = openai.OpenAI()
    response = client.files.create(
        file=combined_training_data,
        purpose="fine-tune"
    )
    return response


import json


# Function to convert JSON bytes to JSONL bytes
def json_to_jsonl(json_bytes):
    # Decode JSON bytes to JSON string
    json_str = json_bytes.decode('utf-8')

    # Parse JSON string
    data = json.loads(json_str)

    # Convert JSON data to JSONL string (each JSON object in a separate line)
    jsonl_str = '\n'.join(json.dumps(obj) for obj in data)

    # Encode JSONL string to bytes
    jsonl_bytes = jsonl_str.encode('utf-8')

    return jsonl_bytes




def training_file_upload(text):
    file_names = similarity(text)

    # Combine training data from files
    combined_training_data = {'training': []}
    for file_name in file_names:
        with open(f'train/{file_name}', 'r') as file:
            data = json.load(file)
            combined_training_data['training'].extend(data.get('training', []))

    # Upload combined training data
    prompt_completion_list= combined_training_data['training']

    chat_completion_list = []

    for i in prompt_completion_list:
        x = {"messages": [{"role": "system", "content": "You are a helpful assistant."},
                          {"role": "user", "content": i['prompt']},
                      {"role": "assistant", "content": i['completion']}]}
        chat_completion_list.append(x)
    print(chat_completion_list)
    chat_completion_list = chat_completion_list
    data = json_to_jsonl(json.dumps((chat_completion_list)).encode())
    print(data)

    response = upload_training_data(data)
    return response.id





def create_model(text):
    file_id = training_file_upload(text)
    client = OpenAI()
    r = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo"
    )
    return r.id

def get_model_id(job_id):
    client = openai.OpenAI()
    done = False
    while done == False:
        x = client.fine_tuning.jobs.retrieve(job_id)
        if x.finished_at != None:
            done = True

    return x.fine_tuned_model

def use_model(model_id,text):
    client = openai.OpenAI()
    response = client.chat.completions.create(
      model=model_id,
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text}
      ]
    )
    return response.choices[0].message.content
