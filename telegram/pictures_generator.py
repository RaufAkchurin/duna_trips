import os
from dotenv import load_dotenv
from openai import OpenAI


def picture_generator(prompt: str):
    load_dotenv()
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=f"watercolor-style image depicting a scene in {prompt}",
            size="1024x1024",
            quality="hd",
            style="vivid",
            n=1,
        )

        image_url = response.data[0].url
        return image_url

    except Exception:
        return None
