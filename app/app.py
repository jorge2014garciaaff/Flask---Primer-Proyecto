import psycopg2
from flask import Flask, render_template, request, url_for, redirect, jsonify

app=Flask(__name__)

@app.before_request
def before_request():
   print("antes de la peticion......")

@app.after_request
def after_request(response):
   print("despues de la peticion..")
   return response

@app.route('/')
def index():
   #return "<h1> ¡hola mundo 2! </h1>"
   cursos= ['Pyhton', 'java', 'html', 'c++', 'php']
   data={
      'titulo':'Primera pagina',
      'bienvenido': 'Hooolaaaaaaa',
      'cursos': cursos,
      'numero_curso': len(cursos)
   }
   return render_template('index.html', data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
   data = {
         'titulo' : 'Contacto',
         'nombre' : nombre,
         'edad' : edad
   }
   return render_template('contacto.html', data=data)

def query_string():
   print(request)
   print(request.args)
   print(request.args.get('param1'))
   print(request.args.get('param2'))
   return "ok"

@app.route('/paciente')
def listar_paciente():
   data = {}
   try:
      connection = psycopg2.connect(
         host='localhost',
         user='postgres',
         password='12345',
         database='postgres'
      )
      print("Conexion exitosa")
      cursor = connection.cursor()

      connection.commit()
      cursor.execute("SELECT nro_paciente, apellido_paciente FROM paciente")
      pacientes = cursor.fetchall()
      #print(pacientes)
      data['pacientes'] = pacientes
      data['mensaje'] = 'Exito'
      # row=cursor.fetchone()
      # print(row)

   except Exception as ex:
      data['mensaje'] = 'Error'
   finally:
      return jsonify(data)
      connection.close()
      print("Conexion finalizada")

def pagina_no_encontrada(error):
   #return render_template('404.html'), 404
   return redirect(url_for('index'))

if __name__ == '__main__':
   app.add_url_rule('/query_string', view_func=query_string)
   app.register_error_handler(404,pagina_no_encontrada)
   app.run(debug=True)