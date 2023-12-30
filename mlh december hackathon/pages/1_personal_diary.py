import streamlit as st
import redis
import pandas as pd
import time
import os
from datetime import datetime
from streamlit_option_menu import option_menu
from localStoragePy import localStoragePy
from pathlib import Path

def save_data(key, data):
    with open(f"data/{key}.txt", "w") as file:
        file.write(data)

def load_data(key):
    try:
        with open(f"data/{key}.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""
    
def get_saved_dates():
    try:
        files = [f.split(".txt")[0] for f in os.listdir("data") if f.endswith(".txt")]
        return sorted(files)
    except FileNotFoundError:
        return []


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
            options=["Today", "Browse Old Entries"],
            orientation='horizontal'
    )


    if selected=="Today":
        current_diary_entry = st.text_area("Today's Entry (" + today_date + "):", value=load_data(today_date_folder_accessible))
        st.markdown = localStorage.getItem(today_date_folder_accessible)
        if st.button("Save"):
            # generate success message:
            success_message = st.success("Saved.")
            time.sleep(1.5) # wait 2 seconds

            # THIS IS NEW : SETTING IN LOCAL STORAGE
            save_data(today_date_folder_accessible, current_diary_entry)
            success_message.empty()

    elif selected=="Browse Old Entries":
        col1, col2 = st.columns(2)
        # setting what is in each column on page:  
        with col1:
            st.caption(":gray[date:]")
            keys = get_saved_dates()
            for key in keys:
                if st.button(f"Display entry for {key}"):
                    st.write(load_data(key))
        with col2:
            st.caption(":gray[mood:]")
            



if __name__ == '__main__':
    main()
