from flask import Flask, request, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/type")
def type_me():
    return render_template("html/type.html")


@app.route("/<mbti_type>/info")
def type_info(mbti_type):
    return render_template(f"html/type_infos/{mbti_type}_info.html")


if __name__ == "__main__":
    app.run(debug=True)
