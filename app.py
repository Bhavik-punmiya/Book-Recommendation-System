import streamlit as st
import pickle
import numpy as np
from jinja2 import Environment, PackageLoader, select_autoescape

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Setup Jinja2 environment
env = Environment(
    loader=PackageLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

# Load Jinja2 templates
popular_template = env.get_template('popular_books.html')
recommendation_template = env.get_template('recommendation.html')

# Render popular books using Jinja2
st.title("Popular Books")
st.write("This is a list of popular books.")

# Assuming popular_books.html is your template for popular books
popular_html = popular_template.render(popular_df=popular_df.to_dict(orient='records'))
st.markdown(popular_html, unsafe_allow_html=True)

# Recommendation UI
st.title("Book Recommendation")
user_input = st.text_input("Enter a book title to get recommendations:")

if user_input:
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:9]

        # Assuming recommendation.html is your template for recommendations
        recommendations = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            recommendations.append({
                'image_url': temp_df['Image-URL-M'].values[0],
                'title': temp_df['Book-Title'].values[0],
                'author': temp_df['Book-Author'].values[0]
            })

        recommendation_html = recommendation_template.render(recommendations=recommendations)
        st.markdown(recommendation_html, unsafe_allow_html=True)
    except IndexError:
        st.write("No recommendations found for the entered book title.")
