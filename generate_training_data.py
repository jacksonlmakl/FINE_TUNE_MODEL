import openai
import json
import os

class TrainingData:
    def __init__(self, text):
        keys = json.load(open("keys.json"))
        os.environ["OPENAI_API_KEY"] = keys['openai']

        self.text = text

        client = openai.OpenAI()
        example = str({"data": [{"prompt": "","completion": ""}]})
        training_response = client.chat.completions.create(
          model="gpt-3.5-turbo-0125",
          response_format={ "type": "json_object" },
          messages=[
            {"role": "system", "content": "You are going to be given textual information and you must return a "
                                          "training "
                                          "dataset that can be given to the openai API for fine-tuning a language "
                                          "model. "
                                          "The purpose of the training data will be for knowledge retention on the "
                                          "key information from the text. "
                                          f"The output must be JSON. There must be at least 15 records. You must structure like prompt/completion pairs or chat messages. Response should follow the format {example}"},
            {"role": "user", "content": self.text}
          ]
        )

        self.training_data = eval(training_response.choices[0].message.content)['data']
        self.training_id = training_response.id

        embedding_response = client.embeddings.create(
            input=self.text,
            model="text-embedding-3-small"
        )
        self.embeddings = embedding_response.data[0].embedding
        self.output = json.dumps({"training": self.training_data, "embeddings": self.embeddings})
    def save(self):
        data = json.loads(self.output)
        file_name = str(self.training_id)
        with open(f'train/{file_name}.json', 'w') as json_file:
            json.dump(data, json_file)



