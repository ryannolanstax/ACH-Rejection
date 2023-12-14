import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

#image = Image.open('Final_Periodic_App/Stax_Banner.png')

#st.image(image)

st.write("# Welcome to STAX ACH Rejects App")




st.markdown(
    """
    These 2 Apps allow us to review ACH Rejects

    **👈 Select an app from the sidebar** to get started

    If an app isn't working correctly, reach out to Ryan Nolan on
    Slack or email ryan.nolan@fattmerchant.com


"""
)
