# backend/app/gcp_client.py
import os
from google import genai


# Initialize Vertex AI / Gemini client
# Two modes: Gemini Developer API (api_key) OR Vertex AI (vertexai=True + project/location)


def init_genai_client():
if os.getenv("USE_GEMINI_DEV_API", "") == "1":
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
else:
client = genai.Client(vertexai=True, project=os.getenv("GCP_PROJECT"), location=os.getenv("GCP_LOCATION", "us-central1"))
return client


client = init_genai_client()


# Example: call Gemini chat
def gemini_chat(prompt: str, chat_history: list[dict] | None = None):
messages = []
if chat_history:
messages.extend(chat_history)
messages.append({"role": "user", "content": prompt})
response = client.chat.create(messages=messages, model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"))
return response


# Example: create embeddings using EmbeddingGemma
def embedding_genma(texts: list[str]):
# model name can be 'embeddinggemma-300m' or similar available in Vertex AI
model = os.getenv("EMBEDDING_MODEL", "embeddinggemma-300m")
resp = client.embeddings.create(model=model, input=texts)
# resp.data -> list of embedding objects depending on sdk
embeddings = [d.embedding for d in resp.data]
return embeddings