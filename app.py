from flask import Flask
from flask import request
from flask import send_file

from PIL import Image
import requests
from io import BytesIO
from PIL import ImageFilter


app = Flask(__name__)


# def modify(im, w=None, h=None, rot=None, b=False):
#     m_img = im

#     m_img = im.resize((w, h))
#     if(b):
#         m_img = filter(ImageFilter.MaxFilter(3))
#     # m_img = im.rotate(im, rot)
#     # m_img = im.thumbnail(im, rot)

#     return m_img


@app.route("/")
def home():
    if(not request.args.get('img')):
        return "No img"

    img = request.args.get('img')
    response = requests.get(img)
    imgg = Image.open(BytesIO(response.content))

    modified_img = imgg

    # size formating
    if(request.args.get('w') and request.args.get('h')):
        w = int(request.args.get('w'))
        h = int(request.args.get('h'))
        modified_img = modified_img.resize((w, h))

    if(request.args.get('rot')):
        rot = int(request.args.get('rot'))
        modified_img = modified_img.rotate(rot)

    # if(request.args.get('b') != None):
    #     b = request.args.get('b')
    #     modified_img = modified_img.filter(ImageFilter.MaxFilter(3))

    q = 100
    if(request.args.get('q')):
        q = int(request.args.get('q'))

    f = "JPEG"
    if(request.args.get('f')):
        f = request.args.get('f')

    img_io = BytesIO()
    modified_img.save(img_io, f, quality=q)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/'+f.lower())


def serve_pil_image(pil_img, q=100, f="JPEG"):
    print("g", f)
    img_io = BytesIO()
    pil_img.save(img_io, f, quality=q)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/'+f.lower())


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(threaded=True, port=5000)
