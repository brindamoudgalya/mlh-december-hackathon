import streamlit as st
import redis
import pandas as pd
import time
from datetime import datetime
from streamlit_option_menu import option_menu
from localStoragePy import localStoragePy
from pathlib import Path


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
        current_diary_entry = st.text_area("Today's Entry (" + today_date + "):", value=localStorage.getItem(today_date_folder_accessible))
        st.markdown = localStorage.getItem(today_date_folder_accessible)
        if st.button("Save"):
            # generate success message:
            success_message = st.success("Saved.")
            time.sleep(2) # wait 2 seconds

            # THIS IS NEW : SETTING IN LOCAL STORAGE
            localStorage.setItem(today_date_folder_accessible, current_diary_entry)
            success_message.empty()

    elif selected=="Browse Old Entries":
        col1, col2 = st.columns(2)
        current_mood="test"
        # setting what is in each column on page:  
        with col1:
            st.caption(":gray[date:]")
            # CHANGE NAME OF BUTTON TO BE DATES WHEN AN ENTRY IS CREATED.
            #test = localStoragePy.getItem(localStorage, "folder_of_diary_entries")
            #st.markdown(test)
            for item in localStorage.getItem("folder_of_diary_entries").length:
                if st.button(date):
                    st.markdown("hello")
        with col2:
            st.caption(":gray[mood:]")
            st.markdown(current_mood)



if __name__ == '__main__':
    main()
