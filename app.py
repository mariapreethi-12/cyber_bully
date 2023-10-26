import streamlit as st
import api
from model import Model
from time import sleep
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.markdown('<h1 style="text-align:center;color:white;font-weight:bolder;font-size:60px;">CYBER BULLYING PREDICTION APPLICATION</h1>',unsafe_allow_html=True)



def title(text,size,color):
    st.markdown(f'<h1 style="font-weight:bolder;font-size:{size}px;color:{color};text-align:center;">{text}</h1>',unsafe_allow_html=True)

def res(res,text,size,color):

    st.markdown(f'<h1 style="font-weight:bolder;font-size:{size}px;color:{color};">{res}</h1>  <h1 style="font-size:{size}px;">{text}</h1> <hr>',unsafe_allow_html=True)


title("Twitter predictions","40","skyblue")
search_term = st.text_input("Enter a search term for twitter extraction:")

api = api.API()
# model = Model()
sid_obj = SentimentIntensityAnalyzer()




# Create a search button
if st.button("Search"):
    st.write("Searching for:", search_term)

    st.write("Results:")
    tweets = api.getTweetsByKeyword(search_term,10)
    


    sleep(3)

    # pred = model.predict(tweets)

    for i in range(0,len(tweets)):

        s = sid_obj.polarity_scores(tweets[i].text)
        
        result = "CYBER BULLYING"
        color = "crimson"
        neg = s['neg']
        pos = s['pos']
        neu = s['neu']

        if(neu*100==100):
            result="NON CYBER BULLYING"
            color = "limegreen"
        

        # st.write(f"{i+1}: negative :{s['neg']*100}%  positive :{s['pos']*100}%  Neutral:{s['neu']*100}%  : {tweets[i].text}")

        res(result,tweets[i].text,"20",color)

        # st.write(f"{i+1}: {pred[i][0]}% {pred[i][1]} : {tweets[i].text}")

    # for tweet in tweets:
        # st.write(f" {i+1} :{tweets[i].text}")


title("Custom text prediction","40","darkviolet")

custom_text = st.text_input("Enter your text:")

if st.button("Predict"):

    s = sid_obj.polarity_scores(custom_text)

    res = "CYBER BULLYING"
    color = "crimson"
    neg = s['neg']
    pos = s['pos']
    neu = s['neu']

    if(neu*100==100 or pos>neg):
        res="NON CYBER BULLYING"
        color = "limegreen"
    
    # st.write( f"{custom_text}")
    title(custom_text,"25","white")
    title(res,"30",color)

