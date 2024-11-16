import streamlit as st
import tensorflow as tf
import numpy as np

def model_prediction(test_image):
    model = tf.keras.models.load_model('trained_model.keras', compile=False)
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(128,128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    prediction = model.predict(input_arr)
    result_index = np.argmax(prediction)
    return(result_index)


app_mode = st.sidebar.selectbox("Select Page",["Disease Recognition"])


#Prediction Page
if(app_mode=="Disease Recognition"):
    st.header("Disease Recognition")
    test_image = st.file_uploader("Choose an Image:")
    if(st.button("Show Image")):
        st.image(test_image,width=4,use_column_width=True)
    #Predict button
    if(st.button("Predict")):
        st.write("Our Prediction")
        result_index = model_prediction(test_image)
        #Reading Labels
        class_name = ['Apple scab', 'Apple Black rot', 'Apple Cedar apple rust', 'Apple healthy',
                    'Blueberry healthy', 'Cherry (including sour) Powdery mildew', 
                    'Cherry (including sour) healthy', 'Corn (maize) Cercospora leaf spot Gray leaf spot', 
                    'Corn (maize) Common rust', 'Corn (maize) Northern Leaf Blight', 'Corn (maize) healthy', 
                    'Grape Black rot', 'Grape Esca (Black Measles)', 'Grape Leaf blight (Isariopsis Leaf Spot)', 
                    'Grape healthy', 'Orange Haunglongbing (Citrus greening)', 'Peach Bacterial spot',
                    'Peach healthy', 'Pepper, bell Bacterial spot', 'Pepperbell healthy', 
                    'Potato Early blight', 'Potato Late blight', 'Potato healthy', 
                    'Raspberry healthy', 'Soybean healthy', 'Squash Powdery mildew', 
                    'Strawberry Leaf scorch', 'Strawberry healthy', 'Tomato Bacterial spot', 
                    'Tomato Early blight', 'Tomato Late blight', 'Tomato Leaf Mold', 
                    'Tomato Septoria leaf spot', 'Tomato Spider mites Two spotted spider mite', 
                    'Tomato Target Spot', 'Tomato Tomato Yellow Leaf Curl Virus', 'Tomato Tomato mosaic virus',
                      'Tomato healthy']
        st.success("Model is Predicting it's a {}".format(class_name[result_index]))