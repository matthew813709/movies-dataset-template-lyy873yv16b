import os
import pandas as pd
import streamlit as st
import altair as alt

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

def load_data():
    db_path = r"C:\Users\Administrator\Desktop\games.sqbpro"  # Raw string notation
    if not os.path.exists(db_path):
        st.error(f"Database file not found at {db_path}")
        return None
    
    # Your existing code to load data from the SQLite database
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM game_data"  # Adjust your SQL query as needed
    df = pd.read_sql_query(query, conn)
    conn.close()
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
        
        # Altair scatter plot configuration
        scatter_plot2 = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='Year_of_Release:O',
            y='EU_sales:Q',
            color='Platform:N',
            tooltip=['Name', 'Platform', 'Year_of_Release', 'EU_sales']
        ).interactive().properties(
            width=800,
            height=400,
            title='Sales by Year'
        )
        
        # Altair scatter plot configuration
        scatter_plot3 = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='Year_of_Release:O',
            y='JP_sales:Q',
            color='Platform:N',
            tooltip=['Name', 'Platform', 'Year_of_Release', 'JP_sales']
        ).interactive().properties(
            width=800,
            height=400,
            title='Sales by Year'
        )

        st.altair_chart(scatter_plot, use_container_width=True)
        st.altair_chart(scatter_plot2, use_container_width=True)
        st.altair_chart(scatter_plot3, use_container_width=True)
        st.write(filtered_df)  # Show the filtered dataframe

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
    
    # Your existing visualization code here
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
