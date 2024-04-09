import requests

# URL of your Streamlit app
url = "http://your-streamlit-app-url.com"

# Parameters for the API call
params = {
    "user_input": "The Great Gatsby"
}

# Make the API call
response = requests.get(url, params=params)

# Parse the JSON response
data = response.json()

# Use the data as needed
print(data)
