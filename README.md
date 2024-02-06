Here's a README markdown template for your Flask API that handles training data creation, model fine-tuning, and model usage. You can adjust the details as necessary to fit the specifics of your project:

```markdown
# Custom GPT Model Fine-Tuning API

This Flask API enables the creation of training data, fine-tuning of GPT models, and utilization of these fine-tuned models. It's designed to streamline the process of training and deploying custom GPT models, specifically tailored to your data and use case requirements.

## Features

- **Create Training Data:** Convert plain text into training data for a GPT 3.5 model.
- **Create Fine-Tuned Model:** Aggregate similar training files based on cosine similarity to the input text, and use them to fine-tune a GPT 3.6 Turbo model.
- **Retrieve Model ID:** Obtain the model ID for a given job ID, associated with the fine-tuning process.
- **Use Model:** Send a prompt to your custom fine-tuned GPT model and receive its output.

## Installation

Before you begin, ensure you have Python and Flask installed on your machine. You will also need to have the custom modules `similarity` and `generate_training_data` available in your project environment.

1. Clone the repository to your local machine.
2. Install the required dependencies:
   ```bash
   pip install flask
   # Add any other dependencies you might have
   ```

## Usage

To start the Flask server, navigate to the directory containing the API code and run:

```bash
python app.py
```

This will start the server on `http://localhost:5000/` by default.

### API Endpoints

#### Create Training Data

- **Endpoint:** `/create_training_data`
- **Method:** POST
- **Body:** `{"text": "<your_plain_text>"}`
- **Description:** Creates training data from the provided plain text.

#### Create Fine-Tuned Model

- **Endpoint:** `/create_model`
- **Method:** POST
- **Body:** `{"text": "<text_for_similarity_matching>"}`
- **Description:** Initiates the fine-tuning process by aggregating similar training files to the provided text.

#### Get Model ID

- **Endpoint:** `/get_model_id`
- **Method:** GET
- **Query Parameter:** `job_id=<job_id_from_create_model>`
- **Description:** Retrieves the model ID associated with the given job ID.

#### Use Model

- **Endpoint:** `/use_model`
- **Method:** POST
- **Body:** `{"model_id": "<your_model_id>", "text": "<prompt_text>"}`
- **Description:** Sends a prompt to the specified custom fine-tuned GPT model and returns its output.

## Contributing

Contributions to the project are welcome. Please ensure to follow the project's coding standards and submit your pull requests for review.

## License

Specify your project's license here, providing details on how others can use and contribute to your project.

## Contact

For any queries or further assistance with the API, please reach out to [Your Contact Information].
```

This README provides a concise overview of your API, including how to install, run, and make requests to your service. Be sure to replace placeholder texts like `[Your Contact Information]` with actual data relevant to your project.
