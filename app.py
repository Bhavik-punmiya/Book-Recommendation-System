import streamlit as st
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Display popular books
st.title("Popular Books")
st.write("This is a list of popular books.")

for index, row in popular_df.iterrows():
    st.image(row['Image-URL-M'], use_column_width=True)
    st.write(f"**{row['Book-Title']}** by {row['Book-Author']}")
    st.write(f"Ratings: {row['num_ratings']}, Average Rating: {row['avg_rating']}")

# Recommendation UI
st.title("Book Recommendation")
user_input = st.text_input("Enter a book title to get recommendations:")

if user_input:
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:9]

        st.write("Recommended Books:")
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            st.image(temp_df['Image-URL-M'].values[0], use_column_width=True)
            st.write(f"**{temp_df['Book-Title'].values[0]}** by {temp_df['Book-Author'].values[0]}")
    except IndexError:
        st.write("No recommendations found for the entered book title.")
