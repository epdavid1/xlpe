from flask import Flask, render_template, request
import pickle
import numpy as np

model = pickle.load(open("model.pkl", "rb"))

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def predict():
    if request.method == "POST" and "pd" in request.form and "corrosion" in request.form and "load" in request.form:
        try:
            if 0 < float(request.form.get("pd")) < 1:
                pd = float(request.form.get("pd"))
            else:
                return render_template("index.html", prediction="Normalized values must be between 0 and 1")
        except:
            return render_template("index.html", prediction="Normalized values must be between 0 and 1")
        try:
            if 0 < float(request.form.get("corrosion")) < 1:
                corrosion = float(request.form.get("corrosion"))
            else:
                return render_template("index.html", prediction="Normalized values must be between 0 and 1")
        except:
            return render_template("index.html", prediction="Normalized values must be between 0 and 1")
        try:
            if int(request.form.get("load")) > 0:
                load = int(request.form.get("load"))
            else:
                return render_template("index.html", prediction="Peak loading must be a positive integer")
        except:
            return render_template("index.html", prediction="Peak loading must be a positive integer")

        defect_dict = {"significant": 0, "minor": 0, "moderate": 0, "serious": 0}
        defect = request.form.get("defect")
        defect_dict[defect] = 1

        features = np.array([[pd, corrosion, load, defect_dict["significant"], defect_dict["minor"],
                              defect_dict["moderate"], defect_dict["serious"]]])
        prediction = str(np.round(model.predict(features)[0], 1))

        return render_template("index.html", prediction="Approximately " + prediction + " years old")

    else:
        return render_template("index.html")


app.run(debug=False)
