# IMPORTING LIBRARIES
import os
from numpy import void
import streamlit as st
import asyncio
import logging
from httpx_oauth.clients.google import GoogleOAuth2
from dotenv import load_dotenv

load_dotenv('.env')
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = os.environ['REDIRECT_URI']


async def get_authorization_url(client: GoogleOAuth2, redirect_uri: str):
    authorization_url = await client.get_authorization_url(redirect_uri, scope=["profile", "email"])
    return authorization_url
    return redirect(f"http://bankereaze.chat:5000/chat")


async def get_access_token(client: GoogleOAuth2, redirect_uri: str, code: str):
    token = await client.get_access_token(code, redirect_uri)
    return token


async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email


def get_login_str():
    client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
    authorization_url = asyncio.run(get_authorization_url(client, REDIRECT_URI))
    google_logo = '<a target="_self" href="{}"><img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" alt="Google Login" width="136" height="46"></a>'.format(authorization_url)

    # google_logo = '<a target="_self" href="{}"><img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" alt="Google Login"></a>'.format(authorization_url)
    return google_logo



# def display_user():
#     query_params = st.experimental_get_query_params()
#     code = query_params.get('code', None)
    
#     if code:
#         # You have the 'code' parameter, proceed with getting the access token and user information.
#         client: GoogleOAuth2 = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)
#         try:
#             token = asyncio.run(get_access_token(client, REDIRECT_URI, code))
#             user_id, user_email = asyncio.run(get_email(client, token['access_token']))
#             st.write(f"You're logged in as {user_email} and id is {user_id}")
#         except Exception as e:
#             logging.error(f"Error in display_user: {str(e)}")
#     else:
#         # Handle the case where the 'code' parameter is not present.
#         st.write("Authentication failed. Please try again.")
        
def authenticate(email, password):
    pass


