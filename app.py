from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Diccionario para almacenar las variables por tipo de dato
variables_por_tipo = {
    'entero': [],
    'real': [],
    'cadena': [],
    'lógico': [],
    'fecha': []
}

# Función para validar la sentencia
def validar_sentencia(sentencia):
    patron = r"^declare\s+([a-zA-Z][\w]*\s*(,\s*[a-zA-Z][\w]*)*)\s+(entero|real|cadena|lógico|fecha)\s*;$"
    coincidencia = re.match(patron, sentencia)
    if coincidencia:
        lista_variables, tipo_dato = coincidencia.groups()[0], coincidencia.groups()[2]
        # Separar las variables por comas
        variables = [var.strip() for var in lista_variables.split(',')]
        for var in variables:
            if validar_identificador(var):
                # Almacenar la variable en la lista correspondiente al tipo de dato
                variables_por_tipo[tipo_dato].append(var)
            else:
                return False  # Si algún identificador es inválido, devolvemos False
        return True
    return False

# Función para validar el identificador de una variable
def validar_identificador(identificador):
    patron_identificador = r"^[a-zA-Z][\w]{0,14}$"
    return bool(re.match(patron_identificador, identificador))

# Ruta principal para validar las sentencias
@app.route("/", methods=["GET", "POST"])
def home():
    resultado = ""
    if request.method == "POST":
        sentencia = request.form.get("sentencia")
        if validar_sentencia(sentencia):
            resultado = "La sentencia es válida."
        else:
            resultado = "La sentencia es inválida."
    return render_template("index.html", resultado=resultado)

# Ruta para consultar variables por tipo de dato
@app.route("/variables", methods=["GET", "POST"])
def consultar_variables():
    variables = []
    tipo_dato = ""
    if request.method == "POST":
        tipo_dato = request.form.get("tipo_dato")
        variables = variables_por_tipo.get(tipo_dato, [])
    return render_template("variables.html", tipo_dato=tipo_dato, variables=variables)

if __name__ == "__main__":
    app.run(debug=True)
