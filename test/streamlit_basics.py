import streamlit as st

st.title("Streamlit Intro")
st.write("This is where we will learn streamlit")

name = st.text_input("What is your name?")
if name:
    st.write(f"Welcome, {name}! Ready to build something amazing")


age = st.slider("Your age",0,100)
gender = st.radio("Gender",("Male","Female","Other"))
interest = st.selectbox("Intrested in",("CV","ML","Both"))

if st.button("Create Profile"):
    st.write(f"Age:{age},Gender:{gender},Interest:{interest}")

# Save user profile without session state
all_profile = []

new_profile = { "Name":name,
                "Age":age,
                "Gender":gender,
                "Interest":interest}


all_profile.append(new_profile)

if st.button("Show current profile"):
    st.write(all_profile)

# Save user profile with session state
if "profiles" not in st.session_state:
    st.session_state.profiles = []

new_profile = { "Name":name,
                "Age":age,
                "Gender":gender,
                "Interest":interest}

if st.button("Save and show profile"):
    st.session_state.profiles.append(new_profile)

st.write(f"All profiles : ", st.session_state.profiles)