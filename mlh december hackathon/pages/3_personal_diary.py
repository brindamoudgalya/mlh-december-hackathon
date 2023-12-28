import streamlit as st
import redis
import pandas as pd
import time
from datetime import datetime
from streamlit_option_menu import option_menu


def main():

    st.title("Personal Diary")

    # change view based on what menu button user clicks
    today_date = datetime.now().strftime("%m/%d/%Y")
    menu = ["Today", "Browse Old Entries"]
    choice = st.sidebar.selectbox("Which entry/entries would you like to visit?", menu)
    if choice == "Today":
        # layout:
        st.text_area("Today's Entry (" + today_date + "):")
        
        if st.button("Save"):
            # generate success message:
            success_message = st.success("Saved.")
            time.sleep(2) # wait 2 seconds
            success_message.empty()


    elif choice == "Browse Old Entries":
        # layout:
        date = st.date_input("date: ", value="today", format="MM/DD/YYYY")

if __name__ == '__main__':
    main()
