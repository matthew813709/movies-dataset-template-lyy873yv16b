import os
import pandas as pd
import sqlite3

def load_data():
    db_path = r"C:\Users\Administrator\Desktop\Maryville\games.csv"  # Adjust path as needed
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")
    
    # Read the CSV file using pandas
    df = pd.read_csv(db_path)
    return df
    
def edit_entries(df):
    st.write("### Edit Entries")
    search_query = st.text_input("Search for a game")

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


# Function to load data from SQLite
def load_data():
    conn = sqlite3.connect('path_to_your_database.db')  # Adjust the path as necessary
    query = "SELECT * FROM game_data WHERE Name LIKE '%Mario%' ORDER BY Platform;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
def insert_new_game(name, platform, year_of_release, na_sales):
    conn = sqlite3.connect('path_to_your_database.db')  # Adjust the path as necessary
    cursor = conn.cursor()
    
    query = """
    INSERT INTO game_data (Name, Platform, Year_of_Release, NA_sales) 
    VALUES (?, ?, ?, ?);
    """
    cursor.execute(query, (name, platform, year_of_release, na_sales))
    conn.commit()
    conn.close()

# Example of using load_data function
df = load_data()
print(df)

def main():
    if check_password():
        st.title("PyGame - A video game database")
        df = load_data()
        st.write(df)  # Display the dataframe for debugging
        edit_entries(df)
        
        st.sidebar.header("Filter Options")
        years = st.sidebar.slider("Select Year Range", 1980, 2020, (2000, 2010))
        filtered_df = df[(df['Year_of_Release'] >= years[0]) & (df['Year_of_Release'] <= years[1])]

        scatter_plot = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='Year_of_Release:O',
            y='NA_sales:Q',
            color='Platform:N',
            tooltip=['Name', 'Platform', 'Year_of_Release', 'NA_sales']
        ).interactive().properties(
            width=800,
            height=400,
            title="Sales by Year"
        )

        st.altair_chart(scatter_plot, use_container_width=True)
        st.write(filtered_df)

if __name__ == "__main__":
    main()

# Function to load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/games.csv")
    return df

# Simple user authentication
def check_password():
    def password_entered():
        if st.session_state["password"] == "password123":  
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password in session state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for the user to enter a password
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True
st.title("PyGame - A video game database")
import streamlit as st
import requests

st.title("PyGame - A video game database")



# Show all games
if st.button("Show All Games"):
    response = requests.get(base_url + 'games')
    st.write(response.json())

# Add a game
st.write("### Add a Game")
name = st.text_input("Name")
platform = st.text_input("Platform")
year_of_release = st.number_input("Year of Release", step=1)
na_sales = st.number_input("NA Sales")

if st.button("Add Game"):
    new_game = {
        "Name": name,
        "Platform": platform,
        "Year_of_Release": year_of_release,
        "NA_sales": na_sales
    }
    response = requests.post(base_url + 'games', json=new_game)
    st.write(response.json())
    
# Function to display and edit entries
def edit_entries(df):
    st.write("### Edit Entries")
    
    # Add a search input
    search_query = st.text_input("Search for a game")

    # Filter the game names based on search query (case-insensitive)
    game_names = df['Name'].str.contains(search_query, case=False, na=False)
    filtered_games = df[game_names]
    
    # Selectbox with filtered game names
    selected_game = st.selectbox("Select a Game to Edit", filtered_games['Name'])
    
    if selected_game:
        game_data = df[df['Name'] == selected_game].iloc[0]
        
        # Display current values and input widgets for editing
        new_name = st.text_input("Name", game_data['Name'])
        new_platform = st.text_input("Platform", game_data['Platform'])
        new_year = st.number_input("Year of Release", int(game_data['Year_of_Release']))
        new_na_sales = st.number_input("NA Sales", float(game_data['NA_sales']))
        
        if st.button("Save Changes"):
            # Update the dataframe with the new values
            df.loc[df['Name'] == selected_game, ['Name', 'Platform', 'Year_of_Release', 'NA_sales']] = [new_name, new_platform, new_year, new_na_sales]
            st.success("Entry updated successfully!")
def load_data():
    conn = sqlite3.connect('path_to_your_database.db')  # Adjust the path as necessary
    query = "SELECT Name FROM game_data ORDER BY Platform;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Example of using load_data function
df = load_data()
print(df)

if __name__ == "__main__":
    main()

# Main function
def main():
    if check_password():
        # User authenticated, show main content
        st.title("PyGame - A video game database")

        # Load data
        df = load_data()
        
        # Display and edit entries
        edit_entries(df)
        
        # Sidebar for user input
        st.sidebar.header("Filter Options")

        # Year slider
        years = st.sidebar.slider("Select Year Range", 1980, 2020, (2000, 2010))

        # Filter the data based on the selected year range
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

# Run main function
if __name__ == "__main__":
    main()
