from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import os

api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/")
def queryChatGPT(question: Question):
    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    extra_body={},
    model="deepseek/deepseek-r1-zero:free",
    messages=[
        {
        "role": "user",
        "content": "What is the meaning of life?"
        }
    ]
    )
    response = completion.choices[0].message.content
    print(response)
    return {"response": response}


app.mount("/", StaticFiles(directory="static", html=True), name="static")


