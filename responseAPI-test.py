import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv(override=True)

client = AzureOpenAI(
    azure_endpoint=os.getenv("azure_endpoint"),
    api_version=os.getenv("api_version"),
    api_key=os.getenv("api_key"),
    azure_deployment=os.getenv("azure_deployment")
)

response = client.responses.create(
  model=os.getenv("azure_deployment"),
  input=[
      {
          "role": "user",
          "content": "Write a one-sentence bedtime story about a unicorn."
      }
  ]
)

print(response.output_text)