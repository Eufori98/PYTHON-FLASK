from flask import Flask, render_template, request, redirect, url_for
import pymysql.cursors

app = Flask(__name__)

mysql = pymysql.connect(host='www.db4free.net',
                             user='dwes_peco',
                             password='5c41f207',
                             database='despliegue_mysql')

@app.route('/')
def index():
    cur = mysql.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT videojuego_id, videojuegos.nombre, videojuegos.precio, plataforma.imagen FROM videojuegos, plataforma WHERE videojuegos.plataforma_id = plataforma.plataforma_id ORDER BY videojuego_id')
    data = cur.fetchall()
    print(data)
    return render_template("index.html", videojuegos = data)

@app.route('/', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        plataforma = request.form['plataforma']
        cur = mysql.cursor()
        cur.execute('INSERT INTO videojuegos (nombre, precio, plataforma_id) VALUES (%s, %s, %s)', (nombre, precio, plataforma))
        mysql.commit() 
        
        return redirect(url_for('index'))

@app.route('/editar/<id>')
def edit_contact(id):
    cur = mysql.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM videojuegos WHERE videojuego_id = %s', (id))
    datos = cur.fetchone()
    print(datos)
    return render_template('editar-videojuego.html', videojuego = datos)

@app.route('/actualizar/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        plataforma = request.form['plataforma']
        cur = mysql.cursor(pymysql.cursors.DictCursor)
        cur.execute('UPDATE videojuegos SET nombre = %s, precio = %s, plataforma_id = %s WHERE videojuego_id = %s', (nombre, precio, plataforma, id))
        mysql.commit() 
        
        return redirect(url_for('index'))

@app.route('/eliminar/<string:id>')
def delete_contact(id):
    cur = mysql.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM videojuegos WHERE videojuego_id = {0}'.format(id))
    mysql.commit() 
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port = 10000, debug = True)