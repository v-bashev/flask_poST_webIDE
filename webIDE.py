from flask import Flask, render_template, redirect, url_for, session, request, send_file
import os, subprocess, uuid

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yXR~XHH!jmN]LWX/,?RT'
subprocess.run("chmod +x translate.sh", shell=True)

def read_from_file(file):
    file = open(file, "r")
    text = file.read()
    file.close()
    return text

def save_code(path, code):
    os.makedirs(path, exist_ok=True)
    if os.path.exists(path + "poST_code.st"):
        subprocess.run("rm " + path + "poST_code.st", shell=True)
        subprocess.run("rm " + path + "poST_code.xml", shell=True)
        subprocess.run("rm " + path + "out", shell=True)
    with open(path + "code.post", "w") as f:
        f.write(code)
        f.close()

def render_index(poST_code, ST_code, out):
    if ST_code is not None:
        return render_template("index.html", poST_code=poST_code, ST_code=ST_code, out=out)
    if out is not None:
        return render_template("index.html", poST_code=poST_code, out=out, disable_ST="disabled", disable_XML="disabled")
    return render_template("index.html", poST_code=poST_code, disable_ST="disabled", disable_XML="disabled")

def load_example(path, file):
    poST_code=read_from_file(file)
    save_code(path, poST_code)
    return render_index(poST_code, None, None)

@app.route('/', methods=["POST"])
def post_methods():
    user_path = 'sessions/' + str(session['user']) + '/'
    if request.form["action"] == "translate":  
        poST_code = request.form["poST_code"]
        save_code(user_path, poST_code)
        subprocess.run("./translate.sh " + str(session['user']), shell=True)
        ST_code = None
        if os.path.exists(user_path + "poST_code.st"):
            ST_code = read_from_file(user_path + "poST_code.st")
        out = read_from_file(user_path + "out")
        return render_index(poST_code, ST_code, out)
    elif request.form["action"] == "openPoST" and 'file' in request.files:
        input_file = request.files["file"]
        poST_code = input_file.read(4 * 1024 * 1024 + 1).decode("utf-8")
        save_code(user_path, poST_code)
        return render_index(poST_code, None, None)
    elif request.form["action"] == "programEmpty":
        return load_example(user_path, "poST_example/empty.post")
    elif request.form["action"] == "programDryer":
        return load_example(user_path, "poST_example/dryer.post")
    elif request.form["action"] == "programElevator":
        return load_example(user_path, "poST_example/elevator.post")
    elif request.form["action"] == "downloadPoST":
        return send_file(user_path + "code.post", attachment_filename='code.post', as_attachment=True)
    elif request.form["action"] == "downloadST":
        return send_file(user_path + "poST_code.st", attachment_filename='poST_code.st', as_attachment=True)
    elif request.form["action"] == "downloadXML":
        return send_file(user_path + "poST_code.xml", attachment_filename='poST_code.xml', as_attachment=True)
    elif request.form["action"] == "about":
        return redirect(url_for('about'))

@app.route('/', methods=["GET"])
def get_main():
    if 'user' in session:
        user_path = 'sessions/' + str(session['user']) + '/'
        if os.path.exists(user_path + "code.post"):
            poST_code = read_from_file(user_path + "code.post")
            if os.path.exists(user_path + "poST_code.st"):
                ST_code = read_from_file(user_path + "poST_code.st")
                out = read_from_file(user_path + "out")
                return render_index(poST_code, ST_code, out)
            return render_index(poST_code, None, None)
    else:
        session['user'] = uuid.uuid4()
    return render_template("index.html", disable_poST="disabled", disable_ST="disabled", disable_XML="disabled")

@app.route('/about', methods=["GET", "POST"])
def about():
    if request.method == "POST":
        return redirect(url_for('get_main'))
    p = subprocess.run("ls sessions/ | wc -w", shell=True, capture_output=True)
    return render_template("about.html", num=p.stdout.decode("utf-8"))

if __name__ == "__main__":
    app.run()
