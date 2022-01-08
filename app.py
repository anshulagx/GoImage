from os import walk
from flask import Flask
from flask import request
from flask import send_file

from PIL import Image
import requests
from io import BytesIO
from PIL import ImageFilter

from os import environ
import os

from flask_cors import CORS, cross_origin

app = Flask(__name__)
print('Server GoImage!')
ver = environ.get("version")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

if(ver != 'lite'):
    # feat cache
    cache = set()
    for (dirpath, dirnames, filenames) in walk('store'):
        cache = set(filenames)


@app.route("/")
@cross_origin()
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


@app.route('/g/<userid>/<img>', methods=['GET'])
def fetch_github(userid, img):
    repo_name = "goimg"
    url = "https://raw.githubusercontent.com/" + \
        userid+"/"+repo_name+"/main/"+img
    ext = url[url.rindex('.')+1:]

    print(url)
    response = requests.get(url)
    print(response)
    img = Image.open(BytesIO(response.content))
    img_io = BytesIO()
    img.save(img_io, ext)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/'+ext)


# @app.route('/gb/<userid>/<repo>/<img>', methods=['GET'])
# def fetch_github(userid, img, repo):
#     repo_name = repo
#     url = "https://raw.githubusercontent.com/" + \
#         userid+"/"+repo_name+"/main/"+img
#     ext = url[url.rindex('.')+1:]

#     print(url)
#     response = requests.get(url)
#     print(response)
#     img = Image.open(BytesIO(response.content))
#     img_io = BytesIO()
#     img.save(img_io, ext)
#     img_io.seek(0)
#     return send_file(img_io, mimetype='image/'+ext)


@app.route('/save', methods=['GET', 'POST'])
def upload_file():
    if(ver != "lite"):
        if request.method == 'POST':
            if 'file1' not in request.files:
                return 'there is no file1 in form!'
            file1 = request.files['file1']
            ext = file1.filename[file1.filename.rindex('.'):]
            path = os.path.join('save', request.form['name']+ext)
            file1.save(path)
            return path

            return 'ok'
        return '''
        <h1>Upload new File</h1>
        <form method="post" enctype="multipart/form-data">
        <input type="text" name="name">
        <input type="file" name="file1">
        <input type="submit">
        </form>
        '''
    else:
        return "This feature is only available in self hosted version :("


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(threaded=True)
