import pandas as pd
import streamlit as st
import os

# Function to edit entries
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
            df.loc[df['Name'] == selected_game, ['Name', 'Platform', 'Year_of_Release', 'NA_sales']] = \
                [new_name, new_platform, new_year, new_na_sales]
            st.success("Entry updated successfully!")

# Function to load data from CSV
def load_data():
    db_path = "design/games.csv"  # Adjust path as needed
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")
    
    df = pd.read_csv(db_path)
    return df

# Password check function
def check_password():
    def password_entered():
        if st.session_state["password"] == "password123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.error("😕 Password incorrect")
        return False
    else:
        return True

# Main function
def main():
    if check_password():
        st.title("PyGame - A video game database")
        df = load_data()
        st.write(df)  # Show the full dataframe

        edit_entries(df)

        # Filter options in the sidebar
        st.sidebar.header("Filter Options")
        years = st.sidebar.slider("Select Year Range", 1980, 2020, (2000, 2010))
        filtered_df = df[(df['Year_of_Release'] >= years[0]) & (df['Year_of_Release'] <= years[1])]

        # Altair scatter plot configuration
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
        st.write(filtered_df)  # Show the filtered dataframe

if __name__ == "__main__":
    main()
