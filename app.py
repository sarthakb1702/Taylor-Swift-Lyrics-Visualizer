import streamlit as st
import lyricsgenius
from wordcloud import WordCloud
import matplotlib.pyplot as plt

GENIUS_API_TOKEN = "imyDitmjO9dGzp8-q_reNPVhhTUt3epo85QDXguArkrFTk45kvWYsyHK6nCnpZqc0Xh61tQETjwJc8FFS-pYCQ"

genius = lyricsgenius.Genius(GENIUS_API_TOKEN)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]
genius.remove_section_headers = True
genius.verbose = False

st.title("🎤 Taylor Swift Lyrics & Word Cloud")

song_title = st.text_input("Enter a Taylor Swift song title:")

if st.button("Fetch Lyrics"):
    if song_title:
        with st.spinner("Fetching lyrics..."):
            try:
                song = genius.search_song(song_title)
                if song:
                    lyrics = song.lyrics
                    st.subheader("Lyrics")
                    st.text_area("Lyrics", lyrics, height=300)

                    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(lyrics)
                    st.subheader("Word Cloud")
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.error("Song not found or lyrics unavailable.")
            except Exception as e:
                st.error(f"Error fetching lyrics: {e}")
    else:
        st.warning("Please enter a song title.")
