from flask import Flask, Response
import os
import time
import webbrowser
import logging
app = Flask(__name__)


def gen():
    i = 0
    refreshInterval = 0
    updateRefresh = 0
    while True:
        time.sleep(refreshInterval)
        images = get_all_images()
        image_name = images[i]
        im = open('images/' + image_name, 'rb').read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + im + b'\r\n')
        i += 1
        if i >= len(images):
            i = 0

        logging.warning('Streamed image')
        updateRefresh += 1
        if updateRefresh == 2:
            logging.warning("Hit 2 threshold")
            refreshInterval = 180



def get_all_images():
    image_folder = "images"
    images = [img for img in os.listdir(image_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png") or
              img.endswith("gif")]
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
    app.run(host='127.0.0.1', debug=True)