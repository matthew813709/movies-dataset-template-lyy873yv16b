import streamlit as st
import pandas as pd
import altair as alt

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

# Main function
def main():
    if check_password():
        # User authenticated, show main content
        st.title("Protected Content")

        # Load data
        df = load_data()
        
        # Sidebar for user input
        st.sidebar.header("Filter Options")

        # Year slider
        years = st.sidebar.slider("Select Year Range", 1980, 2020, (2000, 2010))

        # Filter the data based on the selected year range
        filtered_df = df[(df['Year_of_Release'] >= years[0]) & (df['Year_of_Release'] <= years[1])]

        # Altair scatter plot configuration
        scatter_plot = alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='Year_of_Release:O',  # Make sure this is object type for ordinal scale
            y='NA_sales:Q',  # Replace 'NA_sales' with the appropriate column if necessary
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
