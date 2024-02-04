# imported libraries
import streamlit as st
from newsapi import NewsApiClient
from datetime import date, timedelta

# basic variables
news_provider_list = ['ABC News', 'ABC News (AU)', 'Aftenposten', 'Al Jazeera English', 'ANSA.it', 'Argaam',
                      'Ars Technica', 'Ary News', 'Associated Press', 'Australian Financial Review', 'Axios',
                      'BBC News', 'BBC Sport', 'Bild', 'Blasting News (BR)', 'Bleacher Report', 'Bloomberg',
                      'Breitbart News', 'Business Insider', 'Business Insider (UK)', 'Buzzfeed', 'CBC News',
                      'CBS News', 'CNN', 'CNN Spanish', 'Crypto Coins News', 'Der Tagesspiegel', 'Die Zeit',
                      'El Mundo', 'Engadget', 'Entertainment Weekly', 'ESPN', 'ESPN Cric Info', 'Financial Post',
                      'Focus', 'Football Italia', 'Fortune', 'FourFourTwo', 'Fox News', 'Fox Sports', 'Globo',
                      'Google News', 'Google News (Argentina)', 'Google News (Australia)', 'Google News (Brasil)',
                      'Google News (Canada)', 'Google News (France)', 'Google News (India)', 'Google News (Israel)',
                      'Google News (Italy)', 'Google News (Russia)', 'Google News (Saudi Arabia)', 'Google News (UK)',
                      'Göteborgs-Posten', 'Gruenderszene', 'Hacker News', 'Handelsblatt', 'IGN', 'Il Sole 24 Ore',
                      'Independent', 'Infobae', 'InfoMoney', 'La Gaceta', 'La Nacion', 'La Repubblica', 'Le Monde',
                      'Lenta', "L'equipe", 'Les Echos', 'Libération', 'Marca', 'Mashable', 'Medical News Today',
                      'MSNBC', 'MTV News', 'MTV News (UK)', 'National Geographic', 'National Review', 'NBC News',
                      'News24', 'New Scientist', 'News.com.au', 'Newsweek', 'New York Magazine', 'Next Big Future',
                      'NFL News', 'NHL News', 'NRK', 'Politico', 'Polygon', 'RBC', 'Recode', 'Reddit /r/all', 'Reuters',
                      'RT', 'RTE', 'RTL Nieuws', 'SABQ', 'Spiegel Online', 'Svenska Dagbladet', 'T3n', 'TalkSport',
                      'TechCrunch', 'TechCrunch (CN)', 'TechRadar', 'The American Conservative', 'The Globe And Mail',
                      'The Hill', 'The Hindu', 'The Huffington Post', 'The Irish Times', 'The Jerusalem Post',
                      'The Lad Bible', 'The Next Web', 'The Sport Bible', 'The Times of India', 'The Verge',
                      'The Wall Street Journal', 'The Washington Post', 'The Washington Times', 'Time', 'USA Today',
                      'Vice News', 'Wired', 'Wired.de', 'Wirtschafts Woche', 'Xinhua Net', 'Ynet']
api_key = '-----------------------------' # A unique api key has ben given to you by news-api more info in readme file 
newsapi = NewsApiClient(api_key=api_key)
today = date.today()
month_ago = today - timedelta(days=29)


# functions defined
def form_callback():
    """
    in streamlit we select some input. from this input
    :return: this function use article_to_publish
    """
    topic = st.session_state.topic
    from_date = st.session_state.start_date
    to_date = st.session_state.end_date
    source = ','.join(st.session_state.news_provider)
    all_articles = newsapi.get_everything(q=topic,
                                          sources=source,
                                          domains='bbc.co.uk,techcrunch.com',
                                          from_param=from_date,
                                          to=to_date,
                                          sort_by='relevancy')
    st.write(','.join(st.session_state.news_provider))
    for i in all_articles['articles']:
        st.write('Provided by: ', i['author'])
        st.write('Publish on: ', i['publishedAt'])
        st.write('Title: ', i['title'])
        st.write('Description: ', i['description'])
        st.write('Link to news: ', i['url'])
        st.write('---------------------------------------------')


with st.form(key='my_form'):
    q = st.text_input('Topic of news', key='topic')
    start_date = st.date_input('from date', key='start_date', max_value=today, min_value=month_ago)
    end_date = st.date_input('to date', key='end_date', max_value=today, min_value=month_ago)
    news_sources = st.multiselect('Select news provider', news_provider_list, key='news_provider')
    submit_button = st.form_submit_button(label='submit', on_click=form_callback)
