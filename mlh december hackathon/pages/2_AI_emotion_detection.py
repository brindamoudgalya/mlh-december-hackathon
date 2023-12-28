from streamlit_option_menu import option_menu
import streamlit as st
import numpy as np
import cv2
import streamlit as st
from tensorflow import keras
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from streamlit_webrtc import VideoTransformerFactory, webrtc_streamer, VideoTransformerBase

import pandas as pd
import numpy as np
import altair as alt

import joblib

pipe_lr = joblib.load(open("model/text_emotion.pkl", "rb"))

emotions_emoji_dict = {"anger": "😠", "disgust": "🤮", "fear": "😨😱", "happy": "🤗", "joy": "😂", "neutral": "😐", "sad": "😔",
                       "sadness": "😔", "shame": "😳", "surprise": "😮"}


def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results[0]


def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results


def main():
    selected = option_menu(
        menu_title=None,
        options=['facial emotion detection','text emotion detection'],
        orientation='horizontal',
    )

    if selected=='facial emotion detection':
        # load model
        emotion_dict = {0:'angry', 1 :'happy', 2: 'neutral', 3:'sad', 4: 'surprise'}
        # load json and create model
        json_file = open('model/emotion_model1.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        classifier = model_from_json(loaded_model_json)

        # load weights into new model
        classifier.load_weights("model/emotion_model1.h5")

        #load face
        try:
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        except Exception:
            st.write("Error loading cascade classifiers")

        class VideoTransformer(VideoTransformerBase):
            def transform(self, frame):
                img = frame.to_ndarray(format="bgr24")

                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(
                    image=img_gray, scaleFactor=1.3, minNeighbors=5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img=img, pt1=(x, y), pt2=(
                        x + w, y + h), color=(255, 0, 0), thickness=2)
                    roi_gray = img_gray[y:y + h, x:x + w]
                    roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
                    if np.sum([roi_gray]) != 0:
                        roi = roi_gray.astype('float') / 255.0
                        roi = img_to_array(roi)
                        roi = np.expand_dims(roi, axis=0)
                        prediction = classifier.predict(roi)[0]
                        maxindex = int(np.argmax(prediction))
                        finalout = emotion_dict[maxindex]
                        output = str(finalout)
                    label_position = (x, y)
                    cv2.putText(img, output, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                return img
            
            st.write("Click on start to use webcam and detect your face emotion")
            webrtc_streamer(key="example", video_transformer_factory=VideoTransformerFactory)

    if selected=='text emotion detection':
        st.subheader("Detect Emotions In Text")

        with st.form(key='my_form'):
            raw_text = st.text_area("Type Here")
            submit_text = st.form_submit_button(label='Submit')

        if submit_text:
            col1, col2 = st.columns(2)

            prediction = predict_emotions(raw_text)
            probability = get_prediction_proba(raw_text)

            with col1:
                st.success("Original Text")
                st.write(raw_text)

                st.success("Prediction")
                emoji_icon = emotions_emoji_dict[prediction]
                st.write("{}:{}".format(prediction, emoji_icon))
                st.write("Confidence:{}".format(np.max(probability)))

            with col2:
                st.success("Prediction Probability")
                #st.write(probability)
                proba_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
                #st.write(proba_df.T)
                proba_df_clean = proba_df.T.reset_index()
                proba_df_clean.columns = ["emotions", "probability"]

                fig = alt.Chart(proba_df_clean).mark_bar().encode(x='emotions', y='probability', color='emotions')
                st.altair_chart(fig, use_container_width=True)






if __name__ == '__main__':
    main()
