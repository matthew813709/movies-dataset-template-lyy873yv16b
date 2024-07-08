import pandas as pd
import altair as alt
import streamlit as st

# Function to load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/games.csv")
    return df

# Simple user authentication
def check_password():
    def password_entered():
        if st.session_state["password"] == "password123":  # Replace with your password
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

# Function to display and edit entries
def edit_entries(df):
    st.write("### Edit Entries")
    
    game_names = df['Name'].unique()
    selected_game = st.selectbox("Select a Game to Edit", game_names)
    
    if selected_game:
        game_data = df[df['Name'] == selected_game].iloc[0]
        
        # Display current values and input widgets for editing
        new_name = st.text_input("Name", game_data['Name'])
        new_platform = st.text_input("Platform", game_data['Platform'])
        new_year = st.number_input("Year of Release", int(game_data['Year_of_Release']))
        new_na_sales = st.number_input("NA Sales", float(game_data['NA_sales']))
        new_jp_sales = st.number_input("JP Sales", float(game_data['JP_sales']))
        new_eu_sales = st.number_input("EU Sales", float(game_data['EU_sales']))
        
        if st.button("Save Changes"):
            # Update the dataframe with the new values
            df.loc[df['Name'] == selected_game, ['Name', 'Platform', 'Year_of_Release', 'NA_sales', 'JP_sales', 'EU_sales']] = [new_name, new_platform, new_year, new_na_sales]
            st.success("Entry updated successfully!")

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
         scatter_plot = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='Year_of_Release:O',
            y='JP_sales:Q',  # Replace 'NA_sales' with the appropriate column if necessary
            color='Platform:N',
            tooltip=['Name', 'Platform', 'Year_of_Release', 'NA_sales']
        ).interactive().properties(
            width=800,
            height=400,
            title="Sales by Year"
        )
         scatter_plot = alt.Chart(filtered_df).mark_circle(size=60).encode(
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

        # Optionally display the filtered dataframe (for debugging or user verification)
        st.write(filtered_df)

# Run main function
if __name__ == "__main__":
    main()
