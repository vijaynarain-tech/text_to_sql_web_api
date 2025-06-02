---
title: Chat Completion API Using Sarvam Model
description: >-
  A step-by-step guide on how to use the Chat Completion API for generating text
  completions using Sarvam
---

# Overview

This notebook provides a step-by-step guide on how to use the **Chat Completion API** for generating text completions using **Sarvam**. It includes instructions for installation, setting up the API key, and making API calls to generate completions.

## 0. Installation

Before you begin, ensure you have the necessary Python libraries installed. Run the following commands to install the required packages:

```python
pip install requests
```

## 1. Import Required Libraries

This section imports the necessary Python libraries for making HTTP requests:

```python
import requests
```

- **requests**: For making HTTP requests to the API.

## 2. Set Up the API Endpoint and Payload

To use the Sarvam API, you need an API key. Follow these steps to set up your API key:

1. **Obtain your API key**: If you don't have an API key, sign up on the [Sarvam AI Dashboard](https://dashboard.sarvam.ai/) to get one.
2. **Replace the placeholder key**: In the code below, replace "YOUR_API_KEY_HERE" with your actual API key.

```python
import os

# Replace with your actual API key
SARVAM_API_KEY = "Bearer YOUR_API_KEY_HERE"
SARVAM_API_URL = "https://api.sarvam.ai/v1/chat/completions"
```

### 2.1 Setting Up the API Headers and Payload

This section defines the headers and payload for the chat completion request:

```python
headers = {
    "Authorization": SARVAM_API_KEY,
    "Content-Type": "application/json",
}

payload = {
    "model": "sarvam-m",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of India?"},
    ],
    "temperature": 0.7,
    "top_p": 1.0,
    "max_tokens": 100,
    "n": 1,
}
```

## 3. Making the API Request

This section demonstrates how to make a request to the Chat Completion API and handle the response:

```python
def get_chat_completion(api_url, headers, payload):
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print("Request failed:", response.status_code, response.text)
            return None
    except Exception as e:
        print(f"Error making request: {e}")
        return None
```

### 3.1 Sending the Request and Processing the Response

```python
# Make the API request
response = get_chat_completion(SARVAM_API_URL, headers, payload)

# Process and display the response
if response:
    reply = response["choices"][0]["message"]["content"]
    print("Response:", reply)
```

Example output:

```json
{
  "id": "20250526_816b21fd-98c4-42c8-884e-086bd9d059e8",
  "model": "sarvam-m",
  "created": 1748266512,
  "usage": {
    "prompt_tokens": 19,
    "completion_tokens": 100,
    "total_tokens": 119
  },
  "choices": [
    {
      "index": 0,
      "finish_reason": "length",
      "message": {
        "role": "assistant",
        "content": "The capital of India is **New Delhi**. It serves as the seat of the central government, housing key institutions like the Rashtrapati Bhavan (President's Office), Parliament, and the Supreme Court. While the British established Delhi as the capital in 1911, and it became the official capital of independent India in 1947, the city's history dates back much further, with roots in ancient civilizations and later rule by empires like the Delhi Sultanate."
      }
    }
  ]
}

```

## 4. Conclusion

This tutorial demonstrated how to use the **Sarvam Chat Completion API** for generating text completions. By following the steps, you can easily integrate the API into your applications for various use cases like chatbots, content generation, and more.

## 5. Additional Resources

For more details, refer to the official **Sarvam API documentation** and join the community for support:

- **Documentation**: [docs.sarvam.ai](https://docs.sarvam.ai/)
- **Community**: [Join the Discord Community](https://discord.gg/hTuVuPNF)

## 6. Final Notes

- Keep your API key secure
- Adjust parameters like temperature and max_tokens based on your use case
- Monitor your API usage and stay within your subscription limits

**Keep Building!** 🚀
