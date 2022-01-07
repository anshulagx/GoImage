from flask import Flask
from flask import request
from flask import send_file

from PIL import Image
import requests
from io import BytesIO


app = Flask(__name__)


def resize(im, w, h):
    im1 = im.resize((w, h))
    return im1


def modify(im, w, h):
    m_img = resize(im, w, h)
    # m_img=somethibg(a,b,c)
    return m_img


@app.route("/")
def home():
    img = request.args.get('img')

    # format = request.args.get('format')
    w = int(request.args.get('w'))
    h = int(request.args.get('h'))

    response = requests.get(img)
    imgg = Image.open(BytesIO(response.content))

    modified_img = modify(imgg, w, h)

    return serve_pil_image(modified_img)


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(debug=True)
