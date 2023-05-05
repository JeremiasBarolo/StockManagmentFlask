#<================================================== Invocaiones ==================================================================>
from flask import Flask, flash , render_template, url_for, redirect,request
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='static')
app.secret_key = 'clave_secreta_flask'


#<================================================== Base de Datos==================================================================>

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = '1234' 
app.config['MYSQL_DB'] = 'stock'

mysql = MySQL(app)

#<================================================== Admin==================================================================>
@app.route('/admin')
def admin():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    
    cursor.close()


    
    return render_template('admin.html',categorias=categorias)

#<================================================== Categorias ==================================================================>
@app.route('/categorias')
def categorias():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias=cursor.fetchall()
    cursor.close()


    
    return render_template('categorias.html',categorias=categorias)

#<================================================== Precios==================================================================>
@app.route('/precios')
def precios():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM productos")
    productos=cursor.fetchall()
    cursor.close()
    
    return render_template('precios.html',productos=productos)



#<================================================== Home ==================================================================>
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY nombre ASC")
    productos=cursor.fetchall()
    cursor.close()

    return render_template('index.html',productos=productos)


#<================================================== Productos ==================================================================>
@app.route('/productos')
def productos():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM productos")
    productos=cursor.fetchall()
    cursor.close()
    return render_template('products.html',productos=productos)


#<================================================== Proveedores ==================================================================>
@app.route('/proveedores')
def proveedores():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM proveedores")
    proveedores=cursor.fetchall()
    cursor.close()

    return render_template('proveedores.html', proveedores=proveedores)

#<================================================== Crear Articulos ==================================================================>

@app.route('/crear-producto', methods=['GET', 'POST'])
def crearProducto():
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias=cursor.fetchall()
    producto={}

    if request.method =='POST':
        #Busqueda de datos del formulario
        if "nombre" in request.form:
            nombre= request.form["nombre"]
        if "cantidad_stock" in request.form:
            cantidad_stock= request.form['cantidad_stock']
        if "marca" in request.form:
            marca= request.form['marca']
        if "costo" in request.form:
            costo= request.form['costo']
        if "precio_de_lista" in request.form:
            precio_lista= request.form['precio_de_lista']
        if "vencimiento" in request.form:
            vencimiento= request.form['vencimiento']
        if "proveedor" in request.form:
            proveedor= request.form['proveedor']
        if "categoria_name" in request.form:
            categoria = request.form['categoria_name']
        print(request.form, categoria)    
        #Conexion a la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO productos VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(nombre,cantidad_stock,marca,costo,precio_lista,vencimiento,proveedor,categoria))
        cursor.connection.commit()

        flash(f'Haz agregado satisfactoriamente el articulo {nombre} a tu inventario.')
        
        #Volver a home
        return redirect(url_for('index'))
    
    return render_template('crear_productos.html', producto=producto, categorias=categorias)

#<================================================== Crear Categoria ==================================================================>

@app.route('/crear-categoria', methods=['GET', 'POST'])
def crearCategoria():
    categorias = {}
    if request.method =='POST':
        #Busqueda de datos del formulario
        if "categoria_name" in request.form:
            nombre = request.form['categoria_name']
        #Conexion a la base de datos
        cursor = mysql.connection.cursor()
        last_id = cursor.lastrowid
        cursor.execute("INSERT INTO categorias VALUES (%s, %s)",(last_id, nombre))
        cursor.connection.commit()

        flash(f'Haz agregado satisfactoriamente la categoria {nombre} a tu inventario.')
        
        #Volver a categorias
        return redirect(url_for('categorias'))
    
    return render_template('crear_categoria.html', categorias=categorias)

#<================================================== Borrar Articulos ==================================================================>
@app.route('/borrar/<nombre1>')
def borrar_articulo(nombre1):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM productos WHERE nombre = %s", (nombre1,))
    mysql.connection.commit()

    flash("El artículo ha sido eliminado.")
    return redirect(url_for('index'))

#<================================================== Borrar Categorias ==================================================================>
@app.route('/borrar/<nombre1>')
def borrar_categoria(nombre1):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM categorias WHERE nombre = %s", (nombre1,))
    mysql.connection.commit()

    flash("La categoria ha sido eliminado.")
    return redirect(url_for('categorias'))

#<================================================== Borrar Proveedores==================================================================>

@app.route('/borrar/<nombre1>')
def borrar_proveedor(nombre1):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM proveedores WHERE nombre = %s", (nombre1,))
    mysql.connection.commit()

    flash("El proveedor ha sido eliminado.")
    return redirect(url_for('proveedores'))

#<================================================== Editar Articulo ==================================================================>
@app.route('/editar/<nombre1>', methods= ['GET', 'POST'])
def editar_articulo(nombre1):

    if request.method =='POST':
        #Busqueda de datos del formulario
        if "nombre" in request.form:
            nombre= request.form["nombre"]
        if "cantidad_stock" in request.form:
            cantidad_stock= request.form['cantidad_stock']
        if "marca" in request.form:
            marca= request.form['marca']
        if "costo" in request.form:
            costo= request.form['costo']
        if "precio_de_lista" in request.form:
            precio_lista= request.form['precio_de_lista']
        if "vencimiento" in request.form:
            vencimiento= request.form['vencimiento']
        if "proveedor" in request.form:
            proveedor= request.form['proveedor']
        if "categoria_name" in request.form:
            categoria = request.form['categoria_name']


        #Editado de los datos
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                cantidad_stock = %s,
                marca = %s,
                costo = %s,                 
                precio_lista = %s,
                vencimiento = %s,
                proveedor = %s,
                categoria = %s
            WHERE nombre = %s

        """, (nombre,cantidad_stock,marca,costo,precio_lista,vencimiento,proveedor,categoria, nombre1))
        cursor.connection.commit()

        flash("El artículo ha sido actualizado.")
        return redirect(url_for('index'))
    
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = %s", (nombre1,))
    producto = cursor.fetchall()
    cursor.execute("SELECT * FROM categorias")
    categorias=cursor.fetchall()
    cursor.close()
    #flash("El artículo ha sido eliminado.")
    return render_template('crear_productos.html', producto=producto[0], categorias=categorias)


#<================================================== Editar Categoria ==================================================================>
@app.route('/editar/<nombre1>', methods= ['GET', 'POST'])
def editar_categoria(nombre1):

    if request.method =='POST':
        #Busqueda de datos del formulario
        if "nombre" in request.form:
            nombre= request.form["nombre"]

        #Editado de los datos
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE categorias
            SET nombre = %s,
            WHERE nombre = %s

        """, (nombre, nombre1))
        cursor.connection.commit()

        flash("La categoria ha sido actualizado.")
        return redirect(url_for('index'))
    
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias=cursor.fetchall()
    cursor.close()
    #flash("El artículo ha sido eliminado.")
    return render_template('crear_categoria.html', categorias=categorias)


#<================================================== Crear Proveedor ==================================================================>

@app.route('/crear-proveedor', methods=['GET', 'POST'])
def crearProveedor():
    proveedor = {}
    if request.method == 'POST':
        # Busqueda de datos del formulario
        nombre = request.form['nombre']
        empresa1 = request.form['empresa1']
        numero_tel = request.form['numero_tel']
        
        # Conexion a la base de datos
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO proveedores VALUES (%s, %s, %s)", (nombre, empresa1, numero_tel))
        cursor.connection.commit()

        flash(f'Se ha agregado satisfactoriamente el proveedor {nombre} a la base de datos.')
        
        # Volver a home
        return redirect(url_for('proveedores'))

    # Si se va a crear un nuevo proveedor, mostrar un formulario vacío
    return render_template('crear_proveedor.html', proveedor=proveedor)

#<================================================== Editar Proveedor ==================================================================>

@app.route('/editar-proveedor/<nombre1>', methods= ['GET', 'POST'])
def editar_proveedor(nombre1):
    
    if request.method =='POST':
        # Busqueda de datos del formulario
        nombre = request.form['nombre']
        empresa1 = request.form['empresa1']
        numero_tel = request.form['numero_tel']

        #Conexion a la base de datos
        cursor = mysql.connection.cursor()
        #Editado de los datos
        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                empresa = %s,
                numero_tel = %s
            WHERE nombre = %s

        """, (nombre,empresa1,numero_tel, nombre1))
        cursor.connection.commit()

        flash("El proveedor ha sido actualizado.")
        return redirect(url_for('proveedores'))
    
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM proveedores WHERE nombre = %s", (nombre1,))
    proveedor = cursor.fetchall()
    cursor.close()
    #flash("El artículo ha sido eliminado.")
    return render_template('crear_proveedor.html', proveedor=proveedor[0])

#<================================================== Search ==================================================================>
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + search_term + '%',))
    resultados = cursor.fetchall()
    cursor.close()
    
    return render_template('search_results.html', results=resultados)

if __name__ == '__main__':
    app.run(debug=True)