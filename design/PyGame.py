import os
import streamlit as st
import pandas as pd
import altair as alt

def load_data():
    csv_path = "/games.csv"  # Path to the CSV file
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
    
    # Visualization using Altair
    scatter_plot = alt.Chart(filtered_df).mark_circle(size=60).encode(
        x='Year_of_Release:O',
        y='NA_sales:Q',
        color='Platform:N',
        tooltip=['Name', 'Platform', 'Year_of_Release', 'NA_sales']
    ).interactive().properties(
        width=800,
        height=400,
        title='Sales by Year'
    )
    
    st.altair_chart(scatter_plot, use_container_width=True)
    
    # Comment section
    display_comments()
    add_comment()

if __name__ == "__main__":
    main()
