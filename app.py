import json
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Lista global com os 10 opcionais do sistema
TODOS_OPCIONAIS = [
    "Direção elétrica progressiva",
    "Central Multimídia de 8\"",
    "Sensor de estacionamento traseiro",
    "Câmera de ré",
    "Seis airbags de série",
    "Bancos em couro premium",
    "Ar-condicionado digital dual zone",
    "Teto solar elétrico",
    "Tracionador 4x4 com reduzida",
    "Piloto automático adaptativo (ACC)"
]

def carregar_carros():
    try:
        with open("carros.json", mode="r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

@app.route("/")
def home():
    carros = carregar_carros()
    random.shuffle(carros)
    return render_template("index.html", carros=carros)

@app.route("/veiculos")
def listar_todos_veiculos():
    carros = carregar_carros()
    random.shuffle(carros)
    return render_template("veiculos.html", carros=carros)

@app.route("/selecionar-marca", methods=["GET", "POST"])
def selecionar_marca():
    carros = carregar_carros()
    marcas = sorted(list(set(c["marca"] for c in carros)))
    marca_escolhida = None
    carros_filtrados = []

    if request.method == "POST":
        marca_escolhida = request.form.get("marca")
        if marca_escolhida:
            carros_filtrados = [c for c in carros if c["marca"].lower() == marca_escolhida.lower()]
            random.shuffle(carros_filtrados)

    return render_template("selecionar_marca.html", marcas=marcas, marca_escolhida=marca_escolhida, carros_filtrados=carros_filtrados)

@app.route("/carro/<int:id_carro>")
def detalhe_carro(id_carro):
    carros = carregar_carros()
    carro_encontrado = None

    for carro in carros:
        if carro["id"] == id_carro:
            carro_encontrado = dict(carro)
            # Pega os N primeiros opcionais com base no valor de 'qtd_opcionais'
            qtd = carro_encontrado.get("qtd_opcionais", 3)
            carro_encontrado["opcionais_lista"] = TODOS_OPCIONAIS[:qtd]
            break

    if carro_encontrado:
        return render_template("detalhe_carro.html", carro=carro_encontrado)

    return "<h1>Carro não encontrado!</h1>", 404

if __name__ == "__main__":
    app.run(debug=True)