# Manuar de Utilizacion

Explicaremos como se instala la aplicacion y su utilizacion


## Pre-requisitos 📋

Debemos tener Python 3.7 o superior instalado en el sistema y configurado en las variables de entorno ([aqui](https://tutorial.djangogirls.org/es/python_installation/))

## Instalación 🔧

Para la **Instalacion** debemos descargar primero esta carpeta del repositorio. Una vez descargada abriremos una linea de comandos (CMD, PowerShell,..) y nos hubicamos subre el directorio de la carpeta la carpeta descargada.

Iniciaremos creando un entrono virtual para la aplicacion y asi no afectar nuestro sistema, asi que en la consola ejecutamos el siguiente comando, escogiendo el _nombre_entorno virtual_ que deseemos (**venv** por lo general)

```
python -m venv nombre_entorno_virtual
```

Esperamos que se realice lainstalacion, cuando termine activamos el entorno virtual.

```
.\nombre_entorno virtual\Scripts\activate
```

Nos aparecera al inicio de la linea de comando el nombre del entorno virtual, por ejemplo, en este caso llamamos al entorno virtua **test**.

```
(test) PS C:\PaginaWeb> 
```

Para desactivar el entorno virtual usaremos.

```
deactivate
```

Finalmente instalamos los requisitos necesarios con el comando.

```
pip install -r requirements.txt
```

## Ejecucion 🚀

Ahora ejecutaremos flask para poder acceder a la pagina, asi que con el entorno virtual activado y los requerimientos instalados procedemos a escribir lo siguiente.

```
flask run 
```

Si todo es correcto veremos que podemos acceder a nuestro desarrollo por medio de localhost.

```
* Running on http://127.0.0.1:5000/
```

### Ejecutando las pruebas ⚙️

Ahora accederemos al navegador web y escribimos la direccion de arriba en la barra de direcciones.

```
http://localhost:5000/home
```

Y podremos acceder a la pagina web, el inicio nos mostrara la pagina con los ultimos productos.

![Pagina Inicio](https://i.ibb.co/VLcrj0z/Inicio.png)

Y las categorias

![Categorias](https://i.ibb.co/9NPNsQp/Categorias.png)

Un usuario se podra registrar.

![Registro](https://i.ibb.co/wrfxBtR/Registro.png)

O se prodra logear.

![Login](https://i.ibb.co/BN9s1Pc/Login.png)

El usuario puede seleccionar alguna de las camisetas o navegar entre las caterorias, si selecciona una camiseta tendra la siguietne ventana.

![Producto]((https://i.ibb.co/rcNSYyk/Producto.png)

Podra agregar diferentes productos al carro de compras he ir a el desde l menu de usuario, en el carrito tendra la siguiente vista.

![CarritoCompras](https://i.ibb.co/2YSt8zM/Carrito.png)

### Desinstalacion 🔩

Para quitar la aplicacion simplemente debemos ejecutar el comando de desactivar el entorno virtual

```
deactivate
```

Y eliminar el directorio donde se extrajo la informacion.


## Herramientas 📌

Las siguientes herraientas fueron usadas en el proyecto:


[Python](https://www.python.org/) Python is a programming language that lets you work more quickly and integrate your systems more effectively.  
[Flask](https://flask.palletsprojects.com/en/1.1.x/) Permite crear aplicaciones web rápidamente y con un mínimo número de líneas de código.  
[SQLite](https://www.sqlite.org/index.html) SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.  

## Autores ✒️

_Menciona a todos aquellos que ayudaron a levantar el proyecto desde sus inicios_

* **Nicolas Mendigaño** - *Desarrollo* - [NocolasMend](https://github.com/nicolasMend)
* **Jeison Jara** - *Proyecto* - [JJaraSas](https://github.com/JJaraSas)
* **Alejandro Cortazar**
* **Daniel Medina**

