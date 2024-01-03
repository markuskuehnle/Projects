import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os
import plotly.express as px


# Function to load and process data from SQLite database
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(base_path, '..', 'Scraper', 'Data', 'listings.db')

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM listings", conn)
    conn.close()

    # Sort the data by 'data_id' and 'date' and then drop duplicates
    df.sort_values(by=['data_id', 'date'], inplace=True)
    
    # Get the first occurrence (listing date)
    first_occurrences = df.drop_duplicates(subset=['data_id'], keep='first').rename(columns={'date': 'listing_date'})
    
    # Get the last occurrence (latest date)
    last_occurrences = df.drop_duplicates(subset=['data_id'], keep='last').rename(columns={'date': 'latest_date'})

    # Merge the two dataframes on 'data_id'
    merged_df = pd.merge(first_occurrences, last_occurrences[['data_id', 'latest_date']], on='data_id')

    # Drop the original 'date' columns
    merged_df.drop(columns=['date'], inplace=True, errors='ignore')

    # Add 'status' column
    today_str = datetime.now().strftime("%Y-%m-%d")
    merged_df['status'] = merged_df['latest_date'].apply(lambda x: "listed" if x == today_str else "unlisted")

    return merged_df


def extract_unique_keywords(data):
    keywords = set()
    for criteria in data['secondary_criteria']:
        if criteria:
            keywords.update(criteria.split(', '))
    return list(keywords)


# Function to calculate analytics
def calculate_analytics(data):
    mean_price = data['kaltmiete'].mean()
    mean_living_space = data['living_space'].mean()

    mean_price_by_space = mean_price / mean_living_space
    return mean_price, mean_living_space, mean_price_by_space


# Main function to render the Streamlit dashboard
def main():
    st.title("ImmoScout24 Listings Dashboard")

    # Load data
    data = load_data()

     # Create tabs
    tab1, tab2 = st.tabs(["Data", "Analytics"])

    # Tab 1: Data
    with tab1:
        st.subheader("Listings Data")
        n_all = len(data)
        st.write(f"Number of results: {n_all}")
        st.write(data)

        # Add an interactive plot for price distribution
        fig1 = px.histogram(data, x="kaltmiete", title="Price Distribution")
        st.plotly_chart(fig1)

    # Tab 2: Analytics
    with tab2:
        # Filters
        st.write("Filters")
        min_rooms, max_rooms = st.slider("Rooms Range", min_value=float(data['rooms'].min()), max_value=float(data['rooms'].max()), value=(float(data['rooms'].min()), float(data['rooms'].max())), step=0.5)
        min_space, max_space = st.slider("Living Space Range (m²)", min_value=float(data['living_space'].min()), max_value=float(data['living_space'].max()), value=(float(data['living_space'].min()), float(data['living_space'].max())))
        min_price, max_price = st.slider("Price Range (€)", min_value=float(data['kaltmiete'].min()), max_value=float(data['kaltmiete'].max()), value=(float(data['kaltmiete'].min()), float(data['kaltmiete'].max())), step=50.0)

        # Filter the data based on selections
        filtered_data = data[(data['rooms'] >= min_rooms) & (data['rooms'] <= max_rooms) & 
                             (data['living_space'] >= min_space) & (data['living_space'] <= max_space) & 
                             (data['kaltmiete'] >= min_price) & (data['kaltmiete'] <= max_price)]
        
        # Extract unique keywords for filtering
        unique_keywords = extract_unique_keywords(filtered_data)

        # Multiselect widget for secondary criteria keywords
        selected_keywords = st.multiselect("Filter by Secondary Criteria:", unique_keywords)

        # Address search filter
        address_query = st.text_input("Search in Address")
        if address_query:
            filtered_data = filtered_data[filtered_data['address'].str.contains(address_query, case=False, na=False)]

        # Filter the data based on selected keywords
        if selected_keywords:
            filtered_data = filtered_data[filtered_data['secondary_criteria'].apply(lambda x: any(keyword in x for keyword in selected_keywords))]

        # Status filter for analytics
        status_filter_analytics = st.selectbox("Select Status for Analytics", ["All", "Listed", "Unlisted"])

        if status_filter_analytics == "Listed":
            filtered_data = filtered_data[filtered_data['status'] == 'listed']
        elif status_filter_analytics == "Unlisted":
            filtered_data = filtered_data[filtered_data['status'] == 'unlisted']

        #geocoded_data = get_geocoded_data(filtered_data)

        n = len(filtered_data)
        st.write(f"Number of results: {n}")
        st.write(filtered_data)

        mean_price, mean_living_space, mean_price_by_space = calculate_analytics(filtered_data)
        st.write(f"Mean Price: {mean_price:.2f} €")
        st.write(f"Mean Living Space: {mean_living_space:.2f} m²")
        st.write(f"Mean Price per m²: {mean_price_by_space:.2f} €/m²")

        # Add an interactive plot for price distribution
        fig2 = px.histogram(filtered_data, x="kaltmiete", title="Price Distribution")
        st.plotly_chart(fig2)

        # Display links to listed objects
        st.subheader("Links to Listed Properties")
        listed_properties = filtered_data[filtered_data['status'] == 'listed']
        for index, row in listed_properties.iterrows():
            st.markdown(f"[{row['title']}]({row['expose_url']})")
        
# Run the app
if __name__ == "__main__":
    main()

