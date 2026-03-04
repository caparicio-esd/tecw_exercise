from flask import Flask
from flask import request


app = Flask(__name__)

@app.route('/')
def home():
    return """ 
        <!DOCTYPE html> 
        <html>
        <head>
            <title>Mi Primer Rocódromo</title>
        </head>
        <body>
            <h1>¡Bienvenidx!</h1>
        </body>
        </html>
    """

@app.route('/about')
def about():
    return """ 
        <!DOCTYPE html> 
        <html>
        <head>
            <title>Mi Primer Rocódromo</title>
        </head>
        <body>
            <h1>¡Conócenos un poco más!</h1>
        </body>
        </html>
    """

@app.route('/city/<city>')
def city(city):
    city_upper = city.upper()
    return """ 
        <!DOCTYPE html> 
        <html>
        <head>
            <title>Mi Primer Rocódromo</title>
        </head>
        <body>
            <h1>¡Estamos en {city}!</h1>
        </body>
        </html>
    """.format(city=city_upper)


@app.route('/availability')
def disponibilidad():
    via = request.args.get("via", "-")
    return f""" 
        <!DOCTYPE html> 
        <html>
        <head>
            <title>Mi Primer Rocódromo</title>
        </head>
        <body>
            <h2>La vía de escalada '{via}' está disponible para su uso.</h2>
        </body>
        </html>
    """


if __name__ == '__main__':
    app.run(debug=True)