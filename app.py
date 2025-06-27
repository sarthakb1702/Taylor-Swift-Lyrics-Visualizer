import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os

# --- Safely load Genius API token from secrets or env variable ---
try:
    GENIUS_ACCESS_TOKEN = st.secrets["GENIUS_ACCESS_TOKEN"]
except FileNotFoundError:
    GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

if not GENIUS_ACCESS_TOKEN:
    st.error("Please set the GENIUS_ACCESS_TOKEN in Streamlit secrets or environment variable.")
    st.stop()

# --- Page configuration ---
st.set_page_config(
    page_title="Taylor Swift Lyric Explorer",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_lyrics_from_genius(song_title: str, artist_name: str = "Taylor Swift") -> str | None:
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    search_url = f"{base_url}/search"
    params = {"q": f"{song_title} {artist_name}"}

    try:
        response = requests.get(search_url, params=params, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        
        hits = json_data["response"]["hits"]
        if not hits:
            return None
        
        song_path = hits[0]["result"]["path"]
        song_url = f"https://genius.com{song_path}"

        page = requests.get(song_url)
        soup = BeautifulSoup(page.text, "html.parser")

        lyrics_divs = soup.select("div[data-lyrics-container='true']")
        lyrics = "\n".join(div.get_text(separator="\n") for div in lyrics_divs).strip()

        if not lyrics:
            lyrics_container = soup.find("div", class_="lyrics")
            if lyrics_container:
                lyrics = lyrics_container.get_text(separator="\n").strip()
        
        return lyrics if lyrics else None

    except Exception as e:
        st.error(f"An error occurred while fetching lyrics: {e}")
        return None


def generate_lyrics_wordcloud(lyrics: str) -> plt.Figure:
    stopwords = set(STOPWORDS)
    stopwords.update([
        "verse", "chorus", "bridge", "intro", "outro", "pre", "hook", "post",
        "interlude", "skit", "lyrics", "fade", "out", "song", "yeah", "oh",
        "na", "ah", "hmm", "gonna", "wanna", "da", "la", "like", "just", "dont",
        "know", "can", "will", "get", "got", "cause", "thats", "im", "youre",
        "ive", "weve", "theyre", "its"
    ])

    wordcloud = WordCloud(
        width=1000,
        height=500,
        background_color="white",
        stopwords=stopwords,
        min_font_size=10,
        max_words=200,
        collocations=False
    ).generate(lyrics)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')
    return fig


# --- Streamlit UI ---
st.title("🎶 Taylor Swift Lyric Explorer & Word Cloud Generator")
st.markdown(
    "Unleash your inner Swiftie! Enter any Taylor Swift song title to "
    "fetch its lyrics and visualize the most frequent words in a word cloud."
)

song_input = st.text_input(
    "Enter a Taylor Swift song title:",
    placeholder="e.g., All Too Well",
    help="Type the full song title for best results."
)

if st.button("Get Lyrics & Word Cloud"):
    if song_input:
        with st.spinner(f"Searching for '{song_input}' lyrics..."):
            lyrics = get_lyrics_from_genius(song_input)

        if lyrics:
            st.subheader(f"🎤 Lyrics for '{song_input}'")
            st.text_area(
                "Song Lyrics:",
                lyrics,
                height=300,
                key="lyrics_text_area",
                help="The complete lyrics for the song."
            )

            st.subheader("☁️ Word Cloud from Lyrics")
            with st.spinner("Generating word cloud..."):
                wordcloud_fig = generate_lyrics_wordcloud(lyrics)
                st.pyplot(wordcloud_fig)
                st.markdown(
                    "The word cloud visually represents the most frequent words in the lyrics. "
                    "Larger words appear more often."
                )
        else:
            st.warning(f"Could not find lyrics for '{song_input}'. Please check the spelling or try a different song.")
    else:
        st.info("Please enter a song title to get started!")

st.markdown("---")
