from flask import Flask, Response
import os
import time
import webbrowser
import logging
app = Flask(__name__)

READ_DIR = 'images/' ## <--- Change to directory of desired images

def gen():
    i = 0
    refreshInterval = 0
    updateRefresh = 0
    while True:
        time.sleep(refreshInterval)
        images = get_all_images()
        image_name = images[i]
        im = open(READ_DIR + image_name, 'rb').read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + im + b'\r\n')
        i += 1
        if i >= len(images):
            i = 0

        ## logging.warning('Streamed image') <--- Optional | Only if you want debug confirmation it's finding images
        updateRefresh += 1
        if updateRefresh == 2:
            logging.warning("Hit 2 threshold")
            refreshInterval = 180   ## <-- Change to desired 



 ## Reads directory and turns the paths into a list, then returns them to be incrementally displayed
def get_all_images():
    images = [img for img in os.listdir(READ_DIR)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith(".png") or
              img.endswith(".gif")]
    return images


@app.route('/slideshow')
def slideshow():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return "<html style='background: black; margin: 0px; padding: 0px'><head></head><body><img src='/slideshow' style='width: auto; height: 100%; margin: 0 auto; display: block;'/>" \
           "</body></html>"


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False
