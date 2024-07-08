import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Video Games dataset", page_icon="🎬")
st.title("🎬 Video Games dataset")
st.write(
    """
    This app visualizes data from [The Video Game Database).
    It shows which video game genre performed best over the years. Just 
    click on the widgets below to explore!
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/games.csv")
    return df


df = load_data()

# Display the dataframe in Streamlit
st.write(df)
