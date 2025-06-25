import streamlit as st
import lyricsgenius
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Get your Genius API token and paste below
GENIUS_API_TOKEN = "YOUR_GENIUS_API_TOKEN"

genius = lyricsgenius.Genius(GENIUS_API_TOKEN)

st.title("🎶 Taylor Swift Lyrics & Word Cloud")

# Input for song title
song_title = st.text_input("Enter a Taylor Swift song title:")

if st.button("Fetch Lyrics"):
    if song_title:
        with st.spinner("Fetching lyrics..."):
            try:
                song = genius.search_song(song_title, "Taylor Swift")
                if song:
                    lyrics = song.lyrics
                    st.subheader("Lyrics")
                    st.text_area("Lyrics", lyrics, height=300)

                    # Generate word cloud
                    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(lyrics)
                    st.subheader("Word Cloud")
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.error("Song not found. Please check the title.")
            except Exception as e:
                st.error(f"Error fetching lyrics: {e}")
    else:
        st.warning("Please enter a song title.")
