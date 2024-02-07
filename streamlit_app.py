import openai
import streamlit as st
import requests
import PIL
from PIL import Image
import io

st.set_page_config(page_title="Car Price Prediction", page_icon="pexels-andrew-neel-15863044.jpg")

# sidebar
st.sidebar.image("https://images.pexels.com/photos/15863044/pexels-photo-15863044/free-photo-of-monitor-screen-with-openai-logo-on-black-background.jpeg?auto=compress&cs=tinysrgb&w=600")
# taking input: API key
key = st.sidebar.text_input("Enter Openai API key:")
openai.api_key = key
# All three parts of project
user_selection = st.sidebar.radio("What you want?", ("Sentiment Analysis","Blog Writing","Image Generation"))


# Sentiment Analysis ===================================================================
if user_selection=="Sentiment Analysis":
    st.title("Sentiment Analysis")
    st.subheader("May be your text will be Positive, Negative or Neutral")

    # taking input: Text for performing sentimental analysis
    text = st.text_input("Enter text:")

    def Senitment_analysis(text):
        messages = [
            {"role": "system", "content": """You are trained to analyze and detect the sentiment of given text.
                                            If you're unsure of an answer, you can say "not sure" and recommend users to review manually."""},
            {"role": "user", "content": f"""Analyze the following text and determine if the sentiment is: positive or negative.
                                            Return answer in single word as either positive or negative: {text}"""}
            ]
        response = openai.chat.completions.create(model="gpt-3.5-turbo",
                                                messages=messages,
                                                max_tokens=1,
                                                n=1,
                                                temperature=0)
        response_text = response.choices[0].message.content.strip().lower()
        return response_text

    if st.button("Analyze"):
        if len(text) > 1:
            if len(key)>1:
                st.subheader(f"{Senitment_analysis(text)}")
            else:
                st.sidebar.error("Missing Openai key!")
        else:
            st.error("Missing Text!")


# Blog Writing ===============================================================================
if user_selection=="Blog Writing":
    st.title("Blog Writing")
    # taking input: title of blog
    blog_title = st.text_input("Enter text:")

    def generate_blog(topic):
        messages = [
            {"role": "system", "content": """You are trained to analyze a topic and generate a blog post.
                                            The blog post must contain 1500 to 3000 words (No less than 1500 words)."""},
            {"role": "user", "content": f"""Analyze the topic and generate a blog post. 
                                            Bold every heading and subheadings, much keep writing in 
                                            camel case font style. The topic is {topic}
                                            The blog post should contain the following format.
                                            1) Title (Not more than one line).
                                            2) Introduction (Give introducion about the topic)
                                            3) Body (should describe the facts and findings)
                                            4) General FAQ regarding the topic.
                                            5) Conclusion of the topic. """}
            ]
        response = openai.chat.completions.create(model="gpt-3.5-turbo-16k",
                                                messages=messages,
                                                max_tokens=3000,
                                                n=1,
                                                temperature=0.5)
        response_text = response.choices[0].message.content.strip().lower()
        return response_text

    if st.button("Write Blog"):
        if len(blog_title) > 1:
            if len(key)>1:
                st.write(f"{generate_blog(blog_title)}")
            else:
                st.sidebar.error("Missing Openai key!")
        else:
            st.error("Missing Text!")


# Image Generation ===========================================================================
if user_selection=="Image Generation":
    st.title("Image Generation")
    # taking input: For generating image
    img_text = st.text_input("Enter text:")
    # funtion
    def generate_image_with_prompt(text):
        """
        Generate an image using OpenAI's DALL-E model based on the provided text prompt.

        :param text_prompt: The prompt to generate the image.
        :return: PIL Image object.
        """
        no_of_images = 1
        # Generate Image using OpenAI DALL-E model
        response = openai.images.generate(
                # model="dall-e-3",
                prompt=text,
                n=no_of_images,
                size="1024x1024"
            )
        image_url = response.data[0].url
        # Download image content and convert into PIL
        image_content = requests.get(image_url).content
        image_ = Image.open(io.BytesIO(image_content))
        st.image(image_)
    
    if st.button("Generate Image"):
        if len(img_text) > 1:
            if len(key)>1:
                generate_image_with_prompt(img_text)
            else:
                st.sidebar.error("Missing Openai key!")
        else:
            st.error("Missing Text!")

# End of Code!
