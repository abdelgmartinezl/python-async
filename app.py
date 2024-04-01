from flask import Flask, jsonify, request
from celery import Celery
import time

app = Flask(__name__)

celery = Celery(app.name, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery.task
def sumar(x, y):
    time.sleep(2)
    return x + y

@app.route('/sumar', methods=['POST'])
def sumar_numeros():
    data = request.json
    if 'x' not in data or 'y' not in data:
        return jsonify({'error': 'Faltan datos de entrada'}), 400
    x = data['x']
    y = data['y']
    resultado = sumar.delay(x, y)
    #celery.control.purge()
    return jsonify({'id_tarea': resultado.id}), 202

@app.route('/status/<id_tarea>', methods=['GET'])
def ver_estado_tarea(id_tarea):
    tarea = sumar.AsyncResult(id_tarea)
    if tarea.state == 'PENDING':
        respuesta = {'estado': 'Pendiente'}
    elif tarea.state == 'SUCCESS':
        respuesta = {'estado': 'Exitoso', 'resultado': str(tarea.result)}
    elif tarea.state == 'FAILURE':
        respuesta = {'estado': 'Fallida', 'mensaje': str(tarea.result)}
    else:
        respuesta = {'estado': 'Desconocido'}
    return jsonify(respuesta)


if __name__ == '__main__':
    app.run(debug=True)
