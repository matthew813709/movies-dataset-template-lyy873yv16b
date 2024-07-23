import os
import streamlit as st
import pandas as pd
import altair as alt



def load_data():
    csv_path = "design/games.csv"  # Path to the CSV file
    if not os.path.exists(csv_path):
        st.error(f"CSV file not found at {csv_path}")
        return None
    
    # Load data from the CSV file
    df = pd.read_csv(csv_path)
    return df

def edit_entries(df):
    st.write("### Edit Entries")
    search_query = st.text_input("Search for a game")
    
    if not search_query:
        st.info("Please enter a search term.")
        return
    
    game_names = df['Name'].str.contains(search_query, case=False, na=False)
    filtered_games = df[game_names]
    
    selected_game = st.selectbox("Select a Game to Edit", filtered_games['Name'])
    
    if selected_game:
        game_data = df[df['Name'] == selected_game].iloc[0]
        new_name = st.text_input("Name", game_data['Name'])
        new_platform = st.text_input("Platform", game_data['Platform'])
        new_year = st.number_input("Year of Release", int(game_data['Year_of_Release']))
        new_na_sales = st.number_input("NA Sales", float(game_data['NA_sales']))
        
        if st.button("Save Changes"):
            df.loc[df['Name'] == selected_game, ['Name', 'Platform', 'Year_of_Release', 'NA_sales']] = [new_name, new_platform, new_year, new_na_sales]
            st.success("Entry updated successfully!")

def main():
    st.title("PyGame - A video game database")
    
    df = load_data()
    if df is None:
        return
    
    st.write(df)  # Show the full dataframe
    edit_entries(df)
    
    # Filter options in the sidebar
    st.sidebar.header("Filter Options")
    years = st.sidebar.slider("Select Year Range", 1980, 2020, (2000, 2010))
    filtered_df = df[(df['Year_of_Release'] >= years[0]) & (df['Year_of_Release'] <= years[1])]

# Initialize the session state for comments
if 'comments' not in st.session_state:
    st.session_state['comments'] = []

def display_comments():
    """Display all the comments"""
    st.subheader("Comments Section:")
    for comment in st.session_state['comments']:
        st.write(comment)

def add_comment():
    """Prompt user to add a new comment"""
    st.subheader("Add a Comment")
    new_comment = st.text_area("Write your comment here:")
    if st.button("Submit Comment"):
        if new_comment.strip():
            st.session_state['comments'].append(new_comment)
            st.success("Comment added!")
        else:
            st.error("Comment cannot be empty.")
        st.experimental_rerun()

def main():
    st.title("PyGame - A video game database")
    df = load_data()  # This function should be defined elsewhere in your code
    st.write(df)  # Show the full dataframe
    
    edit_entries(df)  # This function should be defined elsewhere in your code
    
    # Filter options in the sidebar
    st.sidebar.header("Filter Options")
    years = st.sidebar.slider("Select Year Range", 1980, 2020, (2000, 2010))
    filtered_df = df[(df['Year_of_Release'] >= years[0]) & (df['Year_of_Release'] <= years[1])]
    
     # Altair scatter plot configuration
    scatter_plot = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='Year_of_Release:O',
            y='NA_sales:Q',  # Replace 'NA_sales' with the appropriate column if necessary
            color='Platform:N',
            tooltip=['Name', 'Platform', 'Year_of_Release', 'NA_sales']
        ).interactive().properties(
            width=800,
            height=400,
            title="Sales by Year"
        )
    scatter_plot_2 = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='Year_of_Release:O',
            y='JP_sales:Q',  # Replace 'NA_sales' with the appropriate column if necessary
            color='Platform:N',
            tooltip=['Name', 'Platform', 'Year_of_Release', 'NA_sales']
        ).interactive().properties(
            width=800,
            height=400,
            title="Sales by Year"
        )
    scatter_plot_3 = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='Year_of_Release:O',
            y='EU_sales:Q',  # Replace 'NA_sales' with the appropriate column if necessary
            color='Platform:N',
            tooltip=['Name', 'Platform', 'Year_of_Release', 'NA_sales']
        ).interactive().properties(
            width=800,
            height=400,
            title="Sales by Year"
        )

        # Display the scatter plot
st.altair_chart(scatter_plot, use_container_width=True)
st.altair_chart(scatter_plot_2, use_container_width=True)
st.altair_chart(scatter_plot_3, use_container_width=True)

        # Optionally display the filtered dataframe (for debugging or user verification)
st.write(filtered_df)

    # Comment section
display_comments()
add_comment()

if __name__ == "__main__":
    main()
