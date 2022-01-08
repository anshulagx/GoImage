from os import walk
from flask import Flask
from flask import request
from flask import send_file

from PIL import Image
import requests
from io import BytesIO
from PIL import ImageFilter

from os import environ

app = Flask(__name__)

ver = environ.get("version")

if(ver != 'lite'):
    # feat cache
    cache = set()
    for (dirpath, dirnames, filenames) in walk('store'):
        cache = set(filenames)


@app.route("/")
def home():

    f = "JPEG"
    if(request.args.get('f')):
        f = request.args.get('f')

    if(ver != "lite"):
        # feat cache
        if(str(hash(request.url))+"."+f.lower() in cache and request.args.get('img')):
            print('*** Return Cache ***')
            return send_file('store/'+str(hash(request.url))+"."+f.lower(), mimetype='image/'+f.lower())

    img = "https://source.unsplash.com/random"
    if(request.args.get('img')):
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

    if(request.args.get('b')):
        b = request.args.get('b')
        if(b.lower() == "true"):
            modified_img = modified_img.filter(ImageFilter.BLUR)

    q = 100
    if(request.args.get('q')):
        q = int(request.args.get('q'))

    img_io = BytesIO()
    modified_img.save(img_io, f, quality=q)

    if(ver != "lite"):
        # feat cache
        modified_img.save("store/"+str(hash(request.url)) +
                          "."+f.lower(), f, quality=q)
        cache.add(str(hash(request.url)) +
                  "."+f.lower())

    img_io.seek(0)
    return send_file(img_io, mimetype='image/'+f.lower())


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(threaded=True, port=5000)
