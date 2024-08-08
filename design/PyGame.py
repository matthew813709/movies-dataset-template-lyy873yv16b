import os
import streamlit as st
import pandas as pd
import altair as alt
import base64

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

def edit_comment():
    """Edit an existing comment"""
    if 'edit_index' in st.session_state:
        st.subheader("Edit Comment")
        edited_comment = st.text_area("Edit your comment here:", st.session_state['edit_text'])
        if st.button("Save Changes"):
            st.session_state['comments'][st.session_state['edit_index']] = edited_comment
            del st.session_state['edit_index']
            del st.session_state['edit_text']
            st.experimental_rerun()
        if st.button("Cancel"):
            del st.session_state['edit_index']
            del st.session_state['edit_text']
            st.experimental_rerun()
def check_password():
    """Function to check the password and manage the session state"""
    def password_entered():
        if st.session_state["password"] == "password123":  # Set your own password here
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Show the password input if the user hasn't entered a correct password yet
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.error("Password incorrect")
        return False
    else:
        return True

def img_to_bytes(img_path):
    import base64
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

        
def main():
    if check_password():
        st.title("PyGame - A video game database")
        
        # Add Background Image and Set Text Color to White
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url("data:image/png;base64,{img_to_bytes('design/R.jpg')}");
                background-size: cover;
                color: white;
            }}
            .stTextInput > div > div > input {{
                color: black;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Add HomePage Link
        st.markdown("[Homepage](https://www.maryville.edu/)", unsafe_allow_html=True)
        
        df = load_data()
        if df is None:
            return
        
        st.write(df)  # Show the full dataframe
        edit_entries(df)
        
        # Email Registration Section
        register_email()
        
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
            title='Sales by Year (NA_sales)'
        )
        
        st.altair_chart(scatter_plot, use_container_width=True)
        
        # Other visualizations...
        # Initialize the session state for comments
        if 'comments' not in st.session_state:
            st.session_state['comments'] = []
        
        # Comment section
        display_comments()
        edit_comment()
