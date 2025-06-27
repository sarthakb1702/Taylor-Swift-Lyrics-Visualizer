# Taylor Swift Lyrics Visualizer

An interactive web app built with Streamlit that lets you search for Taylor Swift song lyrics and generates a word cloud visualization from the lyrics. Perfect for Swifties and Pythonistas who want to explore the words behind the music!

## Features

- Search for any Taylor Swift song by title
- Fetch lyrics using the Genius API via the `lyricsgenius` Python library
- Display clean and readable song lyrics in a scrollable textbox
- Generate a visually appealing word cloud from the lyrics
- Securely manage the Genius API token using Streamlit Secrets
- Simple, responsive, and user-friendly interface

## Getting Started

### Prerequisites

- Python 3.7 or higher
- A Genius API access token 
### Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/Taylor-Swift-Lyrics-Visualizer.git
cd Taylor-Swift-Lyrics-Visualizer
```
2.Install dependencies:
```bash
pip install -r requirements.txt
```
3.Set up your Genius API token:
```toml
GENIUS_ACCESS_TOKEN = "your_genius_api_access_token_here"
```
or set the environment variable GENIUS_ACCESS_TOKEN on your system.


Running the App Locally
Run the Streamlit app with:
```bash
streamlit run app.py
```

