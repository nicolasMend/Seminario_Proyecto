BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Camisa" (
	"ID_Camisa"	INTEGER NOT NULL UNIQUE,
	"Color"	TEXT NOT NULL,
	"Talla"	TEXT NOT NULL,
	"Precio" NUMERIC,
	"Material" TEXT NOT NULL,
	"TipoCamisa" TEXT NOT NULL
	PRIMARY KEY("ID_Camisa")
);
CREATE TABLE IF NOT EXISTS "CamisaInvetario" (
	"ID_CamisaInventarioPK"	INTEGER NOT NULL UNIQUE,
	"ID_CamisaFK"	INTEGER NOT NULL,
	"ID_InventarioFK"	INTEGER NOT NULL,
	"Fecha"	DATE,
	FOREIGN KEY("ID_CamisaFK") REFERENCES "Camisa"("ID_Camisa"),
	FOREIGN KEY("ID_InventarioFK") REFERENCES "Inventario"("ID_Invetario"),
	PRIMARY KEY("ID_CamisaInventarioPK")
);
CREATE TABLE IF NOT EXISTS "CamisaCompra" (
	"ID_CamisaCompraPK"	INTEGER NOT NULL UNIQUE,
	"ID_CamisaFK"		INTEGER NOT NULL,
	"ID_CompraFK"		INTEGER NOT NULL,
	"VTotalArticulo"	INTEGER NOT NULL,
	"VUnidad"			INTEGER NOT NULL,
	"Cantidad"			
	FOREIGN KEY("ID_CamisaFK") REFERENCES "Camisa"("ID_Camisa"),
	FOREIGN KEY("ID_CompraFK") REFERENCES "Compra"("ID_Compra"),
	PRIMARY KEY("ID_CamisaCompraPK")
);
CREATE TABLE IF NOT EXISTS "Compra" (
	"ID_Compra"		INTEGER NOT NULL UNIQUE,
	"ID_UsuarioFK"	INTEGER NOT NULL,
	"fechaCompra" 	Date,
	"VTotalCompra" 	NUMERIC,
	
	FOREIGN KEY("ID_Usuario") REFERENCES "Usuario"("ID_Usuario"),
	PRIMARY KEY("ID_Compra")
);
CREATE TABLE IF NOT EXISTS "Usuario" (
	"ID_Usuario"	INTEGER UNIQUE,
	"Nombre"		TEXT NOT NULL,
	"Apellido"		TEXT NOT NULL,
	"Edad"			INTEGER NOT NULL,
	"FechaNacimiento"date,
	"Direccion" 	TEXT,
	"Telefono"		INTEGER,
	PRIMARY KEY("ID_Usuario")
);
CREATE TABLE IF NOT EXISTS "Disenador" (
	"ID_Disenador"	INTEGER NOT NULL UNIQUE,
	"Nombre"		TEXT NOT NULL,
	"Apellido"		TEXT NOT NULL,
	"FechaNacimiento"	DATE,
	PRIMARY KEY("ID_Disenador")
);
CREATE TABLE IF NOT EXISTS "Inventario" (
	"ID_InventarioPK"	INTEGER NOT NULL UNIQUE,
	"Lugar"				TEXT NOT NULL,
	"Cantidad" 			INTEGER,
	PRIMARY KEY("ID_Disenador")
);
CREATE TABLE IF NOT EXISTS "Estampa" (
	"ID_Estampa"	INTEGER NOT NULL UNIQUE,
	"ID_Disenador"	INTEGER,
	"Nombre"		TEXT NOT NULL,
	"Descripcion"	TEXT NOT NULL,
	"Imagen1"		TEXT NOT NULL,
	"Imagen2"		TEXT,
	"Imagen3"		TEXT,
	"Tema"			TEXT NOT NULL,
	"Rating"		REAL,
	"ValorEstampa" 	NUMERIC,
	FOREIGN KEY("ID_Disenador") REFERENCES "Disenador"("ID_Disenador"),
	PRIMARY KEY("ID_Estampa")
);
INSERT INTO "Camisa" VALUES (1,'Rojo','M');
INSERT INTO "Camisa" VALUES (4,'verde','L');
INSERT INTO "Camisa" VALUES (5,'Morado','M');
INSERT INTO "Compra" VALUES (1,1,1,1,400);
INSERT INTO "Usuario" VALUES (1,'Alex','Campos',24);
INSERT INTO "Disenador" VALUES (1,'Jose','Mendez',50);
INSERT INTO "Estampa" VALUES (1,1,'Corazon','Estampa de corazon bordeado','https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.xataka.com%2Fmedicina-y-salud%2Fcrean-primer-marcapasos-biodegradable-que-se-disuelve-cuerpo-vez-corazon-late-correctamente&psig=AOvVaw0Z7P0-RFXL32yTk2sZh38u&ust=1629849474870000&source=images&cd=vfe&ved=0CAoQjRxqFwoTCOidjtSsyPICFQAAAAAdAAAAABAD','','','Anatomia',0.2);
COMMIT;
