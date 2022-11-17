from flask import Flask, render_template, flash, request, session,send_file
from flask import render_template, redirect, url_for, request
import warnings
import datetime
import cv2



app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route("/")
def homepage():

    return render_template('index.html')





@app.route("/Test")
def Test():
    return render_template('NewUser.html')










@app.route("/testimage", methods=['GET', 'POST'])
def testimage():
    if request.method == 'POST':


        file = request.files['fileupload']
        file.save('static/Out/Test.jpg')

        img = cv2.imread('static/Out/Test.jpg')
        if img is None:
            print('no data')

        img1 = cv2.imread('static/Out/Test.jpg')
        print(img.shape)
        img = cv2.resize(img, ((int)(img.shape[1] / 5), (int)(img.shape[0] / 5)))
        original = img.copy()
        neworiginal = img.copy()
        cv2.imshow('original', img1)
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        img1S = cv2.resize(img1, (960, 540))

        cv2.imshow('Original image', img1S)
        grayS = cv2.resize(gray, (960, 540))
        cv2.imshow('Gray image', grayS)

        gry = 'static/Out/gry.jpg'

        cv2.imwrite(gry, grayS)
        from PIL import  ImageOps,Image

        im = Image.open(file)

        im_invert = ImageOps.invert(im)
        inv = 'static/Out/inv.jpg'
        im_invert.save(inv, quality=95)

        dst = cv2.fastNlMeansDenoisingColored(img1, None, 10, 10, 7, 21)
        cv2.imshow("Nosie Removal", dst)
        noi = 'static/Out/noi.jpg'

        cv2.imwrite(noi, dst)

        import warnings
        warnings.filterwarnings('ignore')

        import tensorflow as tf
        classifierLoad = tf.keras.models.load_model('model.h5')

        import numpy as np
        from keras.preprocessing import image

        test_image = image.load_img('static/Out/Test.jpg', target_size=(200, 200))
        img1 = cv2.imread('static/Out/Test.jpg')
        # test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifierLoad.predict(test_image)

        print(result)

        out = ''
        fer = ''
        if result[0][0] == 1:

            out = "APPLES"
            fer = '52 calories/1per'

        elif result[0][1] == 1:

            out = "BANANA"
            fer = '100 calories/1per'

        elif result[0][2] == 1:
            out = "ORANGE"
            fer = '50 calories/1per'

        elif result[0][3] == 1:
            out = "PINEAPPLE"
            fer = '60 calories/1per'

        elif result[0][4] == 1:
            out = "WATERMELON"
            fer = '400 calories/1per'




        org = 'static/Out/Test.jpg'





        return render_template('NewUser.html',fer=fer,result=out,org=org)















if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)