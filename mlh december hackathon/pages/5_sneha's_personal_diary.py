import datetime
import streamlit as st
from streamlit_option_menu import option_menu
import firebase_admin
from firebase_admin import firestore, credentials, auth

# Initialize session_state using Streamlit's `SessionState` class
st_session = st.session_state

if 'session' not in st_session:
    st_session.session = None

def init_with_service_account(file_path):
    cred = credentials.Certificate(file_path)
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)
    return firestore.client()

def init_with_project_id(project_id):
    cred = credentials.ApplicationDefault()
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(cred)
    return firestore.client()

def login():
    if st_session.session is not None and st_session.session.login_success:
        # If already logged in, show the main page
        main()
        return

    if 'signedout' not in st_session:
        st_session.signedout = False
    if 'signout' not in st_session:
        st_session.signout = False

    choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
    email = st.text_input('Email Address')
    password = st.text_input('Password', type='password')

    def f(): 
        try:
            user = auth.get_user_by_email(email)
            st_session.session = SessionState(login_success=True, username=user.uid, useremail=user.email)
            st.experimental_rerun()
        except: 
            st.warning('Login Failed')

    def t():
        st_session.session = None
        st_session.signedout = False
        st_session.signout = False   

    if st_session.session is not None and st_session.session.login_success:
        # If logged in, show the main page
        main()
        return
    elif choice == 'Sign up':
        username = st.text_input("Enter your unique username")
        
        if st.button('Create my account'):
            user = auth.create_user(email=email, password=password, uid=username)
            st.success('Account created successfully!')
            st.markdown('Please Login using your email and password')
            st.balloons()
    else:
        if st.button('Login', on_click=f):
            # Login button clicked
            
            if st_session.session is not None and st_session.session.login_success:
            # If logged in, show the main page
                main()

    if st_session.signout:
        if st.button('Sign out', on_click=t):
            st.experimental_rerun()

def main():
    selected = option_menu(
        menu_title=None,
        options=['today', 'previous entries'],
        orientation='horizontal',
        menu_icon='cast',
        icons=['none', 'none']
    )

    if selected == 'today':
        db = firestore.client()
        date = datetime.datetime.now().strftime("%m/%d/%Y")
        key = datetime.datetime.now().strftime("%m/%d/%Y")

        ph = ''
        if st_session.session is None or not st_session.session.login_success:
            ph = 'You must log in or create an account to be able to write in your diary.'
        else:
            ph = 'How are you today?'

        entry_ref = db.collection('Posts').document(st_session.session.username).collection('Entries').document(key)
        entry_data = entry_ref.get()

        if entry_data.exists:
            existing_entry = entry_data.to_dict().get('Content', '')
        else:
            existing_entry = ''

        post = st.text_area(label=date, placeholder=ph, value=existing_entry, height=None, max_chars=500)

        if st.button('save', use_container_width=20):
            if st_session.session is None or not st_session.session.login_success:
                st.warning('You must log in or create an account to be able to create an entry in your diary.')

            # Update or create entry for the day
            entry_ref.set({u'Content': post})
            st.success('Post uploaded!!')

    if selected == 'previous entries':
        db = firestore.client()
        try:
            result = db.collection('Posts').document(st_session.session.username).collection('Entries').stream()

            for entry in result:
                entry_date = entry.id
                entry_data = entry.to_dict()
                content = entry_data.get('Content', '')

                # Format the date label as mm/dd/yyyy
                formatted_date = datetime.datetime.strptime(entry_date, "%Y-%m-%d").strftime("%m/%d/%Y")

                st.text_area(label=formatted_date, value=content)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Define a simple session state class
class SessionState:
    def __init__(self, login_success, username, useremail):
        self.login_success = login_success
        self.username = username
        self.useremail = useremail

if __name__ == "__main__":
    login()
