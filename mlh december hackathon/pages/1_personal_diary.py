import streamlit as st
import redis
import pandas as pd
import time
from datetime import datetime
from streamlit_option_menu import option_menu


def main(): 

    st.title("Personal Diary :notebook:")

    # change view based on what menu button user clicks

    selected = option_menu(
            menu_title=None,
            options=["Today", "Browse Old Entries"],
            orientation='horizontal'
    )

    today_date = datetime.now().strftime("%m/%d/%Y")

    if selected=="Today":
        st.text_area("Today's Entry (" + today_date + "):")
        if st.button("Save"):
            # generate success message:
            success_message = st.success("Saved.")
            time.sleep(2) # wait 2 seconds
            success_message.empty()
    elif selected=="Browse Old Entries":
        col1, col2 = st.columns(2)
        current_mood="test"
        # setting what is in each column on page:  
        with col1:
            st.caption(":gray[date:]")
            # CHANGE NAME OF BUTTON TO BE DATES WHEN AN ENTRY IS CREATED.
            if st.button(datetime.now().strftime("%m/%d/%Y")):
                st.markdown("hello")
        with col2:
            st.caption(":gray[mood:]")
            st.markdown(current_mood)



if __name__ == '__main__':
    main()
