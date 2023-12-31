import joblib
import numpy as np
import streamlit as st
import time
import os
from datetime import datetime
from streamlit_option_menu import option_menu
from localStoragePy import localStoragePy

pipe_lr = joblib.load(open("code/model/text_emotion.pkl", "rb"))

def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results[0]

def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results

def save_data(key, data):
    with open(f"code/data/{key}.txt", "w") as file:
        file.write(data)

def load_data(key):
    st.write(key)
    try:
        with open(f"code/data/{key}.txt", "r") as file:
            return file.read
    except FileNotFoundError:
        return "file not found"

    
def close_data(key):
    try:
        with open(f"code/data/{key}.txt", "r") as file:
            return file.close
    except FileNotFoundError:
        return "file not found"
    
def get_saved_dates():
    try:
        files = [f.split(".txt")[0] for f in os.listdir("code/data") if f.endswith(".txt")]
        return sorted(files)
    except FileNotFoundError:
        return st.write("file not found")


def main(): 

    st.title("Personal Diary :notebook:")

    # access current date:
    today_date = datetime.now().strftime("%m/%d/%Y")
    today_date_folder_accessible = datetime.now().strftime("%m.%d.%Y")

    # setting up local storage: THIS IS NEW ASL;DKFJA;LSDKJFA;SLJFD
    localStorage = localStoragePy("folder_of_diary_entries", 'text')

    # change view based on what menu button user clicks
    selected = option_menu(
            menu_title=None,
            options=["today", "browse old entries"],
            orientation='horizontal',
            menu_icon='cast',
            icons=['','']
    )


    if selected=="today":
        current_diary_entry = st.text_area("Today's Entry (" + today_date + "):", value=load_data(today_date_folder_accessible))
        st.markdown = localStorage.getItem(today_date_folder_accessible)
        if st.button("Save"):
            # generate success message:
            success_message = st.success("Saved.")
            time.sleep(1.5) # wait 2 seconds

            # THIS IS NEW : SETTING IN LOCAL STORAGE
            save_data(today_date_folder_accessible, current_diary_entry)
            success_message.empty()

    elif selected=="browse old entries":
        keys = get_saved_dates()
        st.write(keys)
        for key in keys:
            if st.button(f"Display entry for {key}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(key)
                    st.write(load_data(key))
                with col2:
                    st.caption("mood")
                    prediction = predict_emotions(load_data(key))
                    probability = get_prediction_proba(load_data(key))
                    st.write("{}".format(prediction))
                    st.write("confidence: {}".format(np.max(probability)))

                if st.button("close"):
                    close_data(key)

if __name__ == '__main__':
    main()
