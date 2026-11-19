from flask import Flask, render_template, request, abort

app = Flask(__name__)


# FUNCIÓN UNO: lógica del Ejercicio 1 (notas y asistencia)
def calcular_estado(nota1, nota2, nota3, asistencia):
    """Devuelve (promedio, estado).

    Aprobado solo si promedio >= 40 Y asistencia >= 75.
    """
    promedio = (nota1 + nota2 + nota3) / 3
    if promedio >= 40 and asistencia >= 75:
        estado = "Aprobado"
    else:
        estado = "Reprobado"
    return round(promedio, 1), estado


# FUNCIÓN DOS: lógica del Ejercicio 2 (nombre más largo)
def nombre_mas_largo(nombres):
    """Devuelve (lista_de_ganadores, cantidad_de_letras).

    Cuenta solo letras (ignora espacios). Si hay empate devuelve todos los
    nombres empatados.
    """
    largos = {n: len(n.replace(" ", "")) for n in nombres}
    maximo = max(largos.values())
    ganadores = [n for n, largo in largos.items() if largo == maximo]
    return ganadores, maximo


# RUTAS
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    if request.method == "POST":
        try:
            notas = [float(request.form[f"nota{i}"]) for i in (1, 2, 3)]
            asistencia = float(request.form["asistencia"])
        except (KeyError, ValueError):
            return abort(400)  # datos faltantes o no numéricos

        if any(n < 10 or n > 70 for n in notas):
            return render_template("ejercicio1.html",
                                   error="Las notas deben estar entre 10 y 70.")
        if asistencia < 0 or asistencia > 100:
            return render_template("ejercicio1.html",
                                   error="La asistencia debe estar entre 0 y 100.")

        promedio, estado = calcular_estado(*notas, asistencia)
        return render_template("ejercicio1.html", promedio=promedio,
                               estado=estado, asistencia=asistencia)
    return render_template("ejercicio1.html")


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    if request.method == "POST":
        try:
            nombres = [request.form[f"nombre{i}"].strip() for i in (1, 2, 3)]
        except KeyError:
            return abort(400)

        if not all(nombres):
            return render_template("ejercicio2.html",
                                   error="Debes ingresar los 3 nombres.")
        if len({n.lower() for n in nombres}) < 3:
            return render_template("ejercicio2.html",
                                   error="Los 3 nombres deben ser diferentes.")

        ganadores, cantidad = nombre_mas_largo(nombres)
        return render_template("ejercicio2.html", ganadores=ganadores,
                               cantidad=cantidad)
    return render_template("ejercicio2.html")


@app.errorhandler(400)
def error_400(_error):
    return render_template("error.html", codigo=400,
                           mensaje="Los datos enviados no son válidos."), 400


@app.errorhandler(404)
def error_404(_error):
    return render_template("error.html", codigo=404,
                           mensaje="La página que buscas no existe."), 404


if __name__ == "__main__":
    app.run(debug=True)
