import base64
import io
import json
import os
from io import BytesIO
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from PIL import Image

load_dotenv(override=True)

BLOCKED_DOMAINS = [
    "maliciousbook.com",
    "evilvideos.com",
    "darkwebforum.com",
    "shadytok.com",
    "suspiciouspins.com",
    "ilanbigio.com",
]


def pp(obj):
    print(json.dumps(obj, indent=4))


def show_image(base_64_image):
    image_data = base64.b64decode(base_64_image)
    image = Image.open(BytesIO(image_data))
    image.show()


def calculate_image_dimensions(base_64_image):
    image_data = base64.b64decode(base_64_image)
    image = Image.open(io.BytesIO(image_data))
    return image.size


def sanitize_message(msg: dict) -> dict:
    """Return a copy of the message with image_url omitted for computer_call_output messages."""
    if msg.get("type") == "computer_call_output":
        output = msg.get("output", {})
        if isinstance(output, dict):
            sanitized = msg.copy()
            sanitized["output"] = {**output, "image_url": "[omitted]"}
            return sanitized
    return msg


def create_response(**kwargs):
    url = os.getenv("AZURE_OPENAI_ENDPOINT")
    headers = {
        "Authorization": f"Bearer {os.getenv('AZURE_OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    print(f">>>Request URL: {url}\n")
    print(json.dumps(kwargs, indent=4, ensure_ascii=False))

    response = requests.post(url, headers=headers, json=kwargs)

    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")

    print(f">>>Response: \n")
    print(response.json())
    return response.json()


def check_blocklisted_url(url: str) -> None:
    """Raise ValueError if the given URL (including subdomains) is in the blocklist."""
    hostname = urlparse(url).hostname or ""
    if any(
        hostname == blocked or hostname.endswith(f".{blocked}")
        for blocked in BLOCKED_DOMAINS
    ):
        raise ValueError(f"Blocked URL: {url}")
