import streamlit as st
import redis
import pandas as pd
import time
from datetime import datetime
from streamlit_option_menu import option_menu


def main():

    #connect to Redis database
    redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

    st.title("Personal Diary")
    menu = ["Today", "Browse Old Entries"]
    #choice = st.sidebar.option_menu("Menu", menu)
    with st.sidebar:
        choice = option_menu("Menu", menu, default_index=1)


    # change view based on what menu button user clicks
    today_date = datetime.now().strftime("%m/%d/%Y")
    if choice == "Today":
        # layout:
        current_diary_entry = st.text_area("Today's Entry (" + today_date + "):")
        
        if st.button("Save"):
            # save to Redis database:
            redis_client.rpush('diary_entries', current_diary_entry)

            # generate success message:
            success_message = st.success("Saved.")
            time.sleep(2) # wait 2 seconds
            success_message.empty()


    elif choice == "Browse Old Entries":
        # layout:
        date = st.date_input("date: ", value="today", format="MM/DD/YYYY")

        # display previous entries:
        for i, entry in enumerate(entries, 1):
            st.write(f"{i}. {entry}")

if __name__ == '__main__':
    main()