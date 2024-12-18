import pickle
import pandas as pd  # type: ignore
from flask import Flask, render_template, request  # type: ignore

# Corrección: __name__ en lugar de _name_
app = Flask(__name__)  
app.config["SECRET_KEY"] = "you-will-never-guess"

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=("GET", "POST"))
def index():
    """Main web page"""

    if request.method == "POST":
        user_values = {}

        # Leer valores de las cajas de texto de la interfaz
        user_values["bedrooms"] = float(request.form["bedrooms"])
        user_values["bathrooms"] = float(request.form["bathrooms"])
        user_values["sqft_living"] = float(request.form["sqft_living"])
        user_values["sqft_lot"] = float(request.form["sqft_lot"])
        user_values["floors"] = float(request.form["floors"])

        if request.form.get("waterfront") == "Yes":
            user_values["waterfront"] = 0
        else:
            user_values["waterfront"] = 1

        # Valores entre 1 y 5 para "condition"
        user_values["condition"] = int(request.form.get("condition", 3))

        # Convertir los valores del usuario en un DataFrame
        df = pd.DataFrame.from_dict(user_values, orient="index").T

        # Cargar el modelo desde el archivo pickle
        with open("homework/house_predictor.pkl", "rb") as file:
            loaded_model = pickle.load(file)

        # Predecir el precio de la casa
        prediction = round(loaded_model.predict(df)[0], 2)

    else:
        prediction = None

    # Renderizar la plantilla con la predicción
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)