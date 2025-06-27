import streamlit as st
import lyricsgenius
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import os
import re
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

# --- Page Configuration ---
st.set_page_config(
    page_title="Taylor Swift Lyric Explorer",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- API Key Check ---
if not GENIUS_ACCESS_TOKEN:
    st.error(
        "**Error:** Genius API Access Token not found. "
        "Please set the `GENIUS_ACCESS_TOKEN` environment variable "
        "or add it to Streamlit Secrets (for cloud deployment)."
    )
    st.stop()

# --- Initialize Genius API ---
genius = lyricsgenius.Genius(
    GENIUS_ACCESS_TOKEN,
    verbose=False,
    remove_section_headers=True,
    excluded_terms=["(Live)", "(Acoustic)", "(Remix)"]
)

# --- Function to Fetch Clean Lyrics ---
@st.cache_data
def get_song_lyrics(song_title: str, artist_name: str = "Taylor Swift") -> str | None:
    """
    Fetch and clean lyrics from Genius, removing headers like "123 Contributors", translations, and song blurbs.
    """
    try:
        song = genius.search_song(song_title, artist=artist_name)
        if song:
            lyrics = song.lyrics

            # Remove known endings
            lyrics = re.sub(r'\d+Embed$', '', lyrics).strip()
            lyrics = re.sub(r'You might also like.*?$', '', lyrics, flags=re.DOTALL).strip()

            # Break lyrics into lines
            lines = lyrics.splitlines()

            # Find the first likely lyric line (usually starts with [Verse ...] or actual sentence)
            start_index = 0
            for i, line in enumerate(lines):
                line = line.strip()
                if re.match(r"^\[.*\]$", line):  # e.g., [Verse 1]
                    start_index = i
                    break
                elif len(line.split()) > 3 and line[0].isupper():  # looks like a real lyric line
                    start_index = i
                    break

            lyrics_clean = "\n".join(lines[start_index:]).strip()
            return lyrics_clean
        else:
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching lyrics: {e}")
        return None


# --- Function to Generate Word Cloud ---
@st.cache_data
def generate_lyrics_wordcloud(lyrics: str) -> plt.Figure:
    custom_stopwords = set(STOPWORDS)
    custom_stopwords.update([
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
        stopwords=custom_stopwords,
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

# --- Streamlit App UI ---
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
            lyrics = get_song_lyrics(song_input)

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
