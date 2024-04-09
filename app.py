import streamlit as st
import pickle
import numpy as np
import streamlit.components.v1 as components

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Check if 'user_input' is in session state, if not, set it to an empty string
if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

# Book Recommendation UI
st.title("Book Recommendation")
user_input = st.text_input("Enter a book title to get recommendations:", value=st.session_state.user_input)

if user_input:
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:17]

        recommendations = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            recommendations.append({
                'image_url': temp_df['Image-URL-M'].values[0],
                'title': temp_df['Book-Title'].values[0],
                'author': temp_df['Book-Author'].values[0]
            })

            

        # Prepare HTML content for book recommendations
        html_content = """
        <div class="container">
            <div class="row">
        """
        for rec in recommendations:
            html_content += f"""
            <div class="col-md-3" style="margin-top:50px">
                <div class="card">
                    <div class="card-body">
                        <img class="card-img-top" src="{rec['image_url']}">
                        <p class="text-white">{rec['title']}</p>
                        <h4 class="text-white">{rec['author']}</h4>
                    </div>
                </div>
            </div>
            """
        html_content += """
            </div>
        </div>
        """

        # Render the HTML content
        components.html(html_content, height=600)

    except IndexError:
        st.write("No recommendations found for the entered book title.")

# Update session state with the latest user input
st.session_state.user_input = user_input
