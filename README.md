# Twitter Post Generator

This project integrates Twitter and OpenAI APIs to provide two main functionalities:

1. **Post a 'Make it More' Thread**: Automatically posts a thread on Twitter where each image progressively enhances certain features (e.g., happier, sadder, bigger).
2. **Post Themed Text and Image**: Posts themed stories and corresponding images, like generating horror stories alongside scary images.

## Requirements

- Python 3.8+
- `tweepy`: To interact with the Twitter API
- `openai`: To use OpenAI's API for generating text and modifying images

## Installation

First, clone the repository and install the required packages:

```bash
git clone https://your-repository-url
cd your-project-directory
pip install tweepy openai
```

## Configuration

Before running the application, you need to set up your API keys. Do so in shared_var.py and update it with your credentials.
