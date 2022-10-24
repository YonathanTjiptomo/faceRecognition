from flask import Flask
from flask import jsonify
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

app = Flask(__name__)
@app.route('/yonathan/absensi')
def api_user():

    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model('keras_Model.h5', compile=False)

    # Load the labels
    class_names = ["Yonatham", "Agung", "Nofrets"]

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open('Yonathan.jpg').convert('RGB')
    image = Image.open('agung.png').convert('RGB')
    image = Image.open('nofrets.png').convert('RGB')

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    print('Class: ', class_name, end='')
    print('Confidence Score: ', confidence_score)

    # output
    status = "success"
    user = class_name

    # save data absen

    return jsonify({
        'status': status,
        'user': user
    })