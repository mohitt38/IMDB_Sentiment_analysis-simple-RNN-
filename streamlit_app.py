import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding,SimpleRNN,Dense
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import sequence
import streamlit as st


## Load the imdb datasets
word_index = imdb.get_word_index()
reverse_word_index = {value:key for key, value in word_index.items()}

## Load the pre trained model with Relu activation
model = load_model('simple_rnn_imdb.h5')

# STep 2 : Helper Functions
# Function to decode reviews
def decode_review(encoded_review):
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])


# Function to preprocess user input
def preprocess_text(text):
    words = text.lower().split()
    encoded_review = [word_index.get(word, 2) + 3 for word in words]
    padded_review = sequence.pad_sequences([encoded_review], maxlen=500)
    return padded_review


## Step 3: Prediction Function

def predict_sentence(review):
    preprocessed_input=preprocess_text(review)

    prediction = model.predict(preprocessed_input)

    sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'

    return sentiment , prediction[0][0]


## Streamlit app
st.title('IMDB Movie Review Sentiment Analysis')
st.write('Enter the movie review to classify it as positive or negative. ')

#User input
user_input = st.text_area('Movie Review')

if st.button('Classify'):

    preprocess_input=preprocess_text(user_input)
    
    # Make prediction
    prediction = model.predict(preprocess_input)
    sentiment = 'Positive' if prediction[0][0] > 0.5 else 'Negative'

    # Display the result
    st.write(f'Sentiment: {sentiment}')
    st.write(f'Prediction Score: {prediction[0][0]}')
else:
    st.write('Please enter the movie review')


