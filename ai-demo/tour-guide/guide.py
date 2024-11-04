#RUN: streamlit run guide.py
import os
from openai import OpenAI
import requests
import folium
import streamlit as st
from dotenv import load_dotenv
from streamlit_folium import folium_static

# Load environment variables from the .env file
load_dotenv()

# Get the OpenAI API key from the environment
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Define the function to generate a travel guide
def generate_travel_guide(destination, preferences=""):
    try:
        prompt = f"Create a local tour guide for {destination}. Include information on famous attractions, cultural highlights, and tips. {preferences}"
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="gpt-3.5-turbo"
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error: {e}")
        return "Sorry, I couldn't generate the travel guide at the moment."

# Function to get the coordinates of the destination using Nominatim API
def get_coordinates(destination):
    try:
        nominatim_url = f"https://nominatim.openstreetmap.org/search?format=json&q={destination}"
        response = requests.get(nominatim_url, headers={'User-Agent': 'Mozilla/5.0'})
        location_data = response.json()
        if location_data:
            return {
                "lat": float(location_data[0]["lat"]),
                "lon": float(location_data[0]["lon"])
            }
        else:
            st.warning("Could not find the location. Please try another destination.")
            return None
    except Exception as e:
        st.error(f"Error fetching coordinates: {e}")
        return None

# Function to get nearby places using Overpass API
def get_nearby_places(lat, lon, place_type):
    try:
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        node["{place_type}"](around:2000,{lat},{lon});
        out;
        """
        response = requests.get(overpass_url, params={'data': query})
        data = response.json()
        return data["elements"]
    except Exception as e:
        st.error(f"Error fetching nearby places: {e}")
        return []

# Streamlit app setup
st.title("Travel Buddy and Local Tour Guide")
st.write("Enter a destination, and let your AI Travel Buddy guide you!")

# User input for destination and preferences
destination = st.text_input("Enter a travel destination (e.g., 'Paris', 'Tokyo', 'New York'):")
preferences = st.text_input("Any specific preferences? (e.g., 'food', 'history', 'adventure')")

# Generate travel guide and map button
if st.button("Generate Travel Guide and Map"):
    if destination:
        # Generate the travel guide
        travel_guide = generate_travel_guide(destination, preferences)
        
        # Display the travel guide
        st.subheader(f"Your Travel Guide to {destination.title()}:")
        st.write(travel_guide)
        
        # Get destination coordinates
        coordinates = get_coordinates(destination)
        if coordinates:
            lat, lon = coordinates["lat"], coordinates["lon"]

            # Create a Folium map centered on the destination
            m = folium.Map(location=[lat, lon], zoom_start=13)

            # Add a marker for the main destination
            folium.Marker([lat, lon], tooltip="Main Destination", popup=destination, icon=folium.Icon(color="blue")).add_to(m)

            # Get nearby places for various categories
            categories = {
                "tourism": "green",       # Tourist attractions
                "amenity=restaurant": "red",  # Restaurants
                "public_transport": "purple", # Public transport stations
                "hotel": "orange"          # Hotels
            }

            # Add markers for each category
            all_locations = [[lat, lon]]
            for place_type, color in categories.items():
                places = get_nearby_places(lat, lon, place_type)
                for place in places:
                    place_lat = place["lat"]
                    place_lon = place["lon"]
                    name = place.get("tags", {}).get("name", place_type.replace("_", " ").capitalize())
                    folium.Marker(
                        [place_lat, place_lon],
                        tooltip=name,
                        popup=name,
                        icon=folium.Icon(color=color, icon="info-sign")
                    ).add_to(m)
                    all_locations.append([place_lat, place_lon])

            # Adjust map to fit all markers
            m.fit_bounds(all_locations)

            # Display the map with Folium
            st.subheader("Map of Destination with Points of Interest")
            folium_static(m)
        else:
            st.warning("Could not retrieve coordinates for the specified destination.")
    else:
        st.warning("Please enter a destination.")
