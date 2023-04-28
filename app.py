import streamlit as st
import pandas as pd
from textblob import TextBlob
import requests
import urllib.parse
import time

gnews_api_key = 'API KEY'
ai21_api_key = 'API KEY'

# Streamlit app header
st.title('News Search and Sentiment Analysis')

# User input form
page = st.sidebar.selectbox("Select a page", ["Search", "Top Headlines"])

if page == "Search":
    q = st.text_input('Enter your query:')
    q = urllib.parse.quote(q)
    lang = st.text_input('Enter language (default: en):', 'en')
    country = st.text_input('Enter country (default: us):', 'us')
    max_results = st.number_input('Enter maximum number of results (default: 10):', min_value=1, value=10)
    

    # Search for news articles using GNews API
    if st.button('Search'):
        url = f'https://gnews.io/api/v4/search?q={q}&lang={lang}&country={country}&max={max_results}&token={gnews_api_key}'
        response = requests.get(url)
        data = response.json()
        total_articles = data['totalArticles']
        articles = data['articles']
        if total_articles == 0:
            st.write('No articles found. Please try another search query.')
        else:
            # Sentiment analysis using TextBlob
            for article in articles:
                content = article['content']
                if content:
                    blob = TextBlob(content)
                    polarity = blob.sentiment.polarity
                    if polarity > 0:
                        article['sentiment'] = 'Positive'
                    elif polarity == 0:
                        article['sentiment'] = 'Neutral'
                    else:
                        article['sentiment'] = 'Negative'
                else:
                    article['sentiment'] = 'N/A'

            # Summarize articles using AI21 API
            if ai21_api_key:
                url = 'https://api.ai21.com/studio/v1/summarize'
                headers = {
                    'Authorization': f'Bearer {ai21_api_key}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                for article in articles:
                    content = article['content']
                    if content:
                        payload = {
                            'sourceType': 'TEXT',
                            'source': content,
                            'maxLength': 100,
                            'mode': 'short'
                        }
                        response = requests.post(url, json=payload, headers=headers)
                        data = response.json()
                        data_received = False
                        while not data_received:
                            if 'summary' in data:
                                data_received = True
                            else:
                                time.sleep(0.1)
                        summary = data['summary']
                        article['summary'] = summary
                    else:
                        article['summary'] = 'N/A'

            # Display search results
            df = pd.DataFrame(articles)
            for i in range(len(df)):
                title = df['title'][i]
                summary = df['summary'][i]
                sentiment = df['sentiment'][i]
                url = df['url'][i]
                st.write(f"Title: {title}")
                st.write(f"Summary: {summary}")
                st.write(f"Sentiment: {sentiment}")
                st.write(f"url: {url}")
                st.write("")

elif page == "Top Headlines":
    category = st.text_input('Enter category (default: general):', 'general')
    max_results = st.number_input('Enter maximum number of results (default: 10):', min_value=1, value=10)

    if st.button('Search'):
        url = f'https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&max={max_results}&apikey={gnews_api_key}'
        response = requests.get(url)
        data = response.json()
        total_articles = data['totalArticles']
        articles = data['articles']
        if total_articles == 0:
            st.write('No articles found. Please try another search query.')
        else:
            # Sentiment analysis using TextBlob
            for article in articles:
                content = article['content']
                if content:
                    blob = TextBlob(content)
                    polarity = blob.sentiment.polarity
                    if polarity > 0:
                        article['sentiment'] = 'Positive'
                    elif polarity == 0:
                        article['sentiment'] = 'Neutral'
                    else:
                        article['sentiment'] = 'Negative'
                else:
                    article['sentiment'] = 'N/A'

            # Summarize articles using AI21 API
            if ai21_api_key:
                url = 'https://api.ai21.com/studio/v1/summarize'
                headers = {
                    'Authorization': f'Bearer {ai21_api_key}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                for article in articles:
                    content = article['content']
                    if content:
                        payload = {
                            'sourceType': 'TEXT',
                            'source': content,
                            'maxLength': 100,
                            'mode': 'short'
                        }
                        response = requests.post(url, json=payload, headers=headers)
                        data = response.json()
                        data_received = False
                        while not data_received:
                            if 'summary' in data:
                                data_received = True
                            else:
                                time.sleep(0.1)
                        summary = data['summary']
                        article['summary'] = summary
                    else:
                        article['summary'] = 'N/A'

            # Display search results
            df = pd.DataFrame(articles)
            for i in range(len(df)):
                title = df['title'][i]
                summary = df['summary'][i]
                sentiment = df['sentiment'][i]
                url = df['url'][i]
                st.write(f"Title: {title}")
                st.write(f"Summary: {summary}")
                st.write(f"Sentiment: {sentiment}")
                st.write(f"url: {url}")
                st.write("")
