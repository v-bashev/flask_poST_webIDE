from flask import Flask, render_template, request, send_file, session
import os, subprocess, uuid

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yXR~XHH!jmN]LWX/,?RT'
subprocess.run("chmod +x translate.sh", shell=True)

def send_example(path):
    example_file = open(path)
    example_code = example_file.read()
    example_file.close()
    return render_template("index.html", poST_code=example_code)

def read_from_file(file):
    file = open(file, "r")
    text = file.read()
    file.close()
    return text

@app.route('/', methods=["POST"])
def post_methods():
    if request.form["action"] == "translate":
        user_path = 'sessions/' + str(session['user']) + '/'
        os.makedirs(user_path, exist_ok=True)

        poST_code = request.form["poST_code"]
        with open(user_path + "code.post", "w") as f:
            f.write(poST_code)
            f.close()

        subprocess.run("./translate.sh " + str(session['user']), shell=True)
        
        ST_code = read_from_file(user_path + "code.st")
        out = read_from_file(user_path + "out")
        return render_template("index.html", poST_code=poST_code, ST_code=ST_code, out=out)
    elif request.form["action"] == "programEmpty":
        return send_example("poST_example/empty.post")
    elif request.form["action"] == "programDryer":
        return send_example("poST_example/dryer.post")
    elif request.form["action"] == "programElevator":
        return send_example("poST_example/elevator.post")
    else:
        subprocess.run("rm src-gen.zip", shell=True)
        subprocess.run(["zip", "-r", "src-gen.zip", "src-gen"])
        return send_file("src-gen.zip", attachment_filename='src-gen.zip', as_attachment=True)
        

@app.route('/', methods=["GET"])
def get_main():
    if 'user' in session:
        user_path = 'sessions/' + str(session['user']) + '/'
        if os.path.exists(user_path + "code.post"):
            poST_code = read_from_file(user_path + "code.post")
            ST_code = read_from_file(user_path + "code.st")
            out = read_from_file(user_path + "out")
            return render_template("index.html", poST_code=poST_code, ST_code=ST_code, out=out)
    else:
        session['user'] = uuid.uuid4()
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
