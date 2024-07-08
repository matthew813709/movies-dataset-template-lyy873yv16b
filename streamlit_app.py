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
@st.cache_data
def load_data():
    df = pd.read_csv("data/games.csv")
    return df

# Load data
df = load_data()

# Print column names for verification
st.write("Columns in the dataframe:", df.columns)

st.sidebar.header("Filter Options")

# Year slider
years = st.sidebar.slider("Select Year Range", 1980, 2020, (2000, 2010))

# Verify if 'Year_of_Release' column is present and valid
if 'Year_of_Release' in df.columns:
    # Filter the data based on selected year range
    filtered_df = df[(df['Year_of_Release'] >= years[0]) & (df['Year_of_Release'] <= years[1])]

    # Altair chart configuration
    chart = alt.Chart(filtered_df).mark_line().encode(
        x='Year_of_Release:O',
        y='NA_sales:Q',  # Replace 'NA_sales' with the appropriate column if necessary
        color='Platform:N',
        tooltip=['Name', 'Platform', 'Year_of_Release', 'NA_sales']
    ).interactive().properties(
        width=800,
        height=400,
        title="Sales by Year"
    )

    # Display the chart
    st.altair_chart(chart, use_container_width=True)

    # Display dataframe for verification
    st.write(filtered_df)
else:
    st.write("The 'Year_of_Release' column does not exist in the dataframe")
