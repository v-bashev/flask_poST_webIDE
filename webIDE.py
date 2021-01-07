from flask import Flask, render_template, request, send_file
import subprocess

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        if request.form["action"] == "translate":
            code = request.form["poST_code"]
            code_file = open("code.post", "w")
            code_file.write(code)
            code_file.close()

            subprocess.run("rm -rf src-gen", shell=True)
            p = subprocess.run(["java", "-jar", "post_to_st.jar", "code.post"], capture_output=True, text=True)
            
            subprocess.run("cat src-gen/* > all_code.st", shell=True)
            all_code_file = open("all_code.st", "r")
            all_code = all_code_file.read()
            all_code_file.close()
            subprocess.run("rm all_code.st", shell=True)
            
            ret = p.stdout + p.stderr
            return render_template("index.html", poST_code=code, ST_code=all_code, poST_error=ret)
        elif request.form["action"] == "programEmpty":
            example_file = open("poST_example/empty.post")
            example_code = example_file.read()
            example_file.close()
            return render_template("index.html", poST_code=example_code)
        elif request.form["action"] == "programDryer":
            example_file = open("poST_example/dryer.post")
            example_code = example_file.read()
            example_file.close()
            return render_template("index.html", poST_code=example_code)
        elif request.form["action"] == "programElevator":
            example_file = open("poST_example/elevator.post")
            example_code = example_file.read()
            example_file.close()
            return render_template("index.html", poST_code=example_code)
        else:
            subprocess.run("rm src-gen.zip", shell=True)
            subprocess.run(["zip", "-r", "src-gen.zip", "src-gen"])
            return send_file("src-gen.zip", attachment_filename='src-gen.zip', as_attachment=True)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)