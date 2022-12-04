import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(
    page_title="GitHub Project Recommendation System",
    page_icon="GitHub-icon.png",
)
components.html("""
     <style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative&display=swap');</style>
    <h1 style="color:ZBlack;font-family: 'Cinzel Decorative', cursive;
font-size:30px">Enter the details to Recommend Projects</h1>    """,height=100,width=700)
with st.form(key = "form1"):
      tag1 = st.selectbox('Select Preferred Domain 1 ',('ANDROID', 'JAVA', 'PYTHON'))
      tag2 = st.selectbox('Select Preferred Domain 2 ',('ANDROID', 'JAVA', 'PYTHON'))
      tag3 = st.selectbox('Select Preferred Domain 3 ',('ANDROID', 'JAVA', 'PYTHON'))
      tag4 = st.selectbox('Select Preferred Domain 4 ',('ANDROID', 'JAVA', 'PYTHON'))
      tag5 = st.selectbox('Select Preferred Domain 5 ',('ANDROID', 'JAVA', 'PYTHON'))
      lang = st.selectbox('Select Preferred Language ',('JAVASCRIPT', 'JAVA', 'PYTHON'))
     
      submit = st.form_submit_button(label = "Submit")
      if submit:
        st.write("Details Submitted")
