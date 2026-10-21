
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from pyswip import Prolog

app = Flask(__name__)
CORS(app)

# Localizar la base de conocimientos junto a app.py
BASE_DIR = Path(__file__).resolve().parent
RUTA_PROLOG = BASE_DIR / "recetas.pl"

prolog = Prolog()
prolog.consult(str(RUTA_PROLOG))


@app.route("/api/consultar", methods=["POST"])
def consultar():
    datos = request.get_json(silent=True) or {}

    ingredientes = datos.get("ingredientes", [])
    momento = datos.get("momento", "cualquiera")
    restriccion = datos.get("restriccion", "ninguna")

    if not isinstance(ingredientes, list):
        return jsonify({"error": "Los ingredientes deben ser una lista"}), 400

    if not all(isinstance(i, str) for i in ingredientes):
        return jsonify({"error": "Ingrediente no válido"}), 400

    # Evitar insertar texto del usuario directamente en consultas Prolog.
    ingredientes_validos = {
        "tortillas_de_harina", "tortillas_de_maiz",
        "quesillo_deshebrado", "queso_gouda", "queso_asadero",
        "queso_panela", "pollo_deshebrado", "pollo_asado",
        "pollo_rostizado", "epazote_fresco", "salsa_de_tomate",
        "pepperoni", "vegetales_salteados", "tostadas",
        "dos_jitomates", "caja_de_caldillo_de_tomate",
        "cebolla_en_rodajas", "un_chile_chipotle", "crema",
        "lechuga", "pimiento_morron_salteado", "cebolla_salteada",
        "chile_serrano"
    }

    if not set(ingredientes).issubset(ingredientes_validos):
        return jsonify({"error": "Se recibió un ingrediente desconocido"}), 400

    if momento not in {"cualquiera", "desayuno", "comida", "cena"}:
        return jsonify({"error": "Momento no válido"}), 400

    if restriccion not in {"ninguna", "sin_carne", "sin_lacteos"}:
        return jsonify({"error": "Restricción no válida"}), 400

    # Por ahora consultamos las recetas cuyos ingredientes registrados
    # están todos disponibles. Después añadiremos las reglas de filtros.
    recetas = list(prolog.query("tipo_receta(Receta, _)"))
    nombres = sorted({r["Receta"] for r in recetas})

    return jsonify({"recetas": nombres})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
