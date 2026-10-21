
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from pyswip import Prolog

app = Flask(__name__)
CORS(app)

# Cargar la base de conocimientos existente
BASE_DIR = Path(__file__).resolve().parent
RUTA_PROLOG = (BASE_DIR / "recetas.pl").as_posix()

prolog = Prolog()
prolog.consult(RUTA_PROLOG)


@app.route("/api/consultar", methods=["POST"])
def consultar():
    datos = request.get_json(silent=True) or {}

    ingredientes = datos.get("ingredientes", [])
    momento = datos.get("momento", "cualquiera")
    restriccion = datos.get("restriccion", "ninguna")

    ingredientes_validos = {
        "tortillas_de_harina", "tortillas_de_maiz",
        "quesillo_deshebrado", "queso_gouda",
        "queso_asadero", "queso_panela",
        "pollo_deshebrado", "pollo_asado",
        "pollo_rostizado", "epazote_fresco",
        "salsa_de_tomate", "pepperoni",
        "vegetales_salteados", "tostadas",
        "dos_jitomates", "caja_de_caldillo_de_tomate",
        "cebolla_en_rodajas", "un_chile_chipotle",
        "crema", "lechuga"
    }

    if not isinstance(ingredientes, list):
        return jsonify({"error": "Los ingredientes deben ser una lista"}), 400

    if not all(isinstance(i, str) for i in ingredientes):
        return jsonify({"error": "Ingrediente no válido"}), 400

    if not set(ingredientes).issubset(ingredientes_validos):
        return jsonify({"error": "Ingrediente desconocido"}), 400

    if momento not in {"cualquiera", "desayuno", "comida", "cena"}:
        return jsonify({"error": "Momento no válido"}), 400

    if restriccion not in {"ninguna", "sin_carne", "sin_lacteos"}:
        return jsonify({"error": "Restricción no válida"}), 400

    # Obtener los hechos directamente de Prolog
    requisitos = {}
    for dato in prolog.query(
        "ingrediente_receta(Receta, Ingrediente)"
    ):
        receta = str(dato["Receta"])
        ingrediente = str(dato["Ingrediente"])
        requisitos.setdefault(receta, set()).add(ingrediente)

    categorias = {}
    for dato in prolog.query("tipo_receta(Receta, Tipo)"):
        categorias[str(dato["Receta"])] = str(dato["Tipo"])

    alternativas = {}
    for dato in prolog.query(
        "ingrediente_alternativo(Base, Alternativa)"
    ):
        base = str(dato["Base"])
        alternativa = str(dato["Alternativa"])
        alternativas.setdefault(base, set()).add(alternativa)

    # Normalizar sustitutos conocidos sin modificar recetas.pl
    disponibles = set(ingredientes)

    if "vegetales_salteados" in disponibles:
        disponibles.update({
            "pimiento_morron_salteado",
            "cebolla_salteada",
            "chile_serrano"
        })

    if "pollo_asado" in disponibles or "pollo_rostizado" in disponibles:
        disponibles.add("pollo_deshebrado")

    # Comprobar si cada ingrediente requerido está disponible
    def ingrediente_disponible(requerido):
        if requerido in disponibles:
            return True

        if disponibles.intersection(
            alternativas.get(requerido, set())
        ):
            return True

        # Los tres tipos de pollo se consideran equivalentes
        if requerido == "pollo_deshebrado":
            return bool(disponibles.intersection({
                "pollo_asado", "pollo_rostizado"
            }))

        return False

    recetas_encontradas = []

    for receta, necesarios in requisitos.items():

        # Deben estar disponibles todos los ingredientes requeridos
        if not all(
            ingrediente_disponible(i) for i in necesarios
        ):
            continue

        # Filtrar por momento del día
        if momento != "cualquiera":
            if categorias.get(receta) != momento:
                continue

        # Aplicar restricciones según los hechos de la receta
        if restriccion == "sin_carne":
            if necesarios.intersection({
                "pollo_deshebrado", "pepperoni"
            }):
                continue

        if restriccion == "sin_lacteos":
            if necesarios.intersection({
                "quesillo_deshebrado", "queso_gouda",
                "queso_asadero", "queso_panela", "crema"
            }):
                continue

        recetas_encontradas.append(receta)

    return jsonify({"recetas": sorted(recetas_encontradas)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)


