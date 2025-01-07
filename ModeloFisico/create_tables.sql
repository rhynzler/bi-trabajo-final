
CREATE TABLE agente (
	id_agente SERIAL NOT NULL, 
	id_tipo_agente INTEGER NOT NULL, 
	nombre_tipo VARCHAR NOT NULL, 
	nombre_agente VARCHAR NOT NULL, 
	CONSTRAINT agente_pkey PRIMARY KEY (id_agente)
)

;


CREATE TABLE fecha (
	id_fecha SERIAL NOT NULL, 
	num_anio INTEGER NOT NULL, 
	num_mes INTEGER NOT NULL, 
	num_semana INTEGER NOT NULL, 
	num_dia INTEGER NOT NULL, 
	CONSTRAINT fecha_pkey PRIMARY KEY (id_fecha)
)

;


CREATE TABLE producto (
	id_producto SERIAL NOT NULL, 
	id_division INTEGER NOT NULL, 
	nombre_division VARCHAR NOT NULL, 
	nombre_producto VARCHAR NOT NULL, 
	CONSTRAINT producto_pkey PRIMARY KEY (id_producto)
)

;


CREATE TABLE satisfaccion (
	id_pregunta SERIAL NOT NULL, 
	descripcion VARCHAR NOT NULL, 
	opcion_elegida VARCHAR NOT NULL, 
	CONSTRAINT satisfaccion_pkey PRIMARY KEY (id_pregunta)
)

;


CREATE TABLE calidad (
	calidad_id SERIAL NOT NULL, 
	minutos_esperados INTEGER NOT NULL, 
	id_fecha INTEGER NOT NULL, 
	id_agente INTEGER NOT NULL, 
	id_satisfaccion INTEGER NOT NULL, 
	CONSTRAINT calidad_pkey PRIMARY KEY (calidad_id), 
	CONSTRAINT calidad_id_agente_fkey FOREIGN KEY(id_agente) REFERENCES agente (id_agente), 
	CONSTRAINT calidad_id_fecha_fkey FOREIGN KEY(id_fecha) REFERENCES fecha (id_fecha), 
	CONSTRAINT calidad_id_satisfaccion_fkey FOREIGN KEY(id_satisfaccion) REFERENCES satisfaccion (id_pregunta)
)

;


CREATE TABLE efectividad (
	efectividad_id SERIAL NOT NULL, 
	clientes_atendidos INTEGER NOT NULL, 
	unidades_vendidas INTEGER NOT NULL, 
	monto_vendido DOUBLE PRECISION NOT NULL, 
	precio_unitario DOUBLE PRECISION NOT NULL, 
	minutos_esperados INTEGER NOT NULL, 
	id_fecha INTEGER NOT NULL, 
	id_agente INTEGER NOT NULL, 
	CONSTRAINT efectividad_pkey PRIMARY KEY (efectividad_id), 
	CONSTRAINT efectividad_id_agente_fkey FOREIGN KEY(id_agente) REFERENCES agente (id_agente), 
	CONSTRAINT efectividad_id_fecha_fkey FOREIGN KEY(id_fecha) REFERENCES fecha (id_fecha)
)

;


CREATE TABLE retroalimentacion (
	retroalimentacion_id SERIAL NOT NULL, 
	clientes_atendidos INTEGER NOT NULL, 
	unidades_vendidas INTEGER NOT NULL, 
	monto_vendido DOUBLE PRECISION NOT NULL, 
	precio_unitario DOUBLE PRECISION NOT NULL, 
	minutos_esperados INTEGER NOT NULL, 
	id_agente INTEGER NOT NULL, 
	id_satisfaccion INTEGER NOT NULL, 
	CONSTRAINT retroalimentacion_pkey PRIMARY KEY (retroalimentacion_id), 
	CONSTRAINT retroalimentacion_id_agente_fkey FOREIGN KEY(id_agente) REFERENCES agente (id_agente), 
	CONSTRAINT retroalimentacion_id_satisfaccion_fkey FOREIGN KEY(id_satisfaccion) REFERENCES satisfaccion (id_pregunta)
)

;


CREATE TABLE ventas (
	ventas_id SERIAL NOT NULL, 
	unidades_vendidas INTEGER NOT NULL, 
	monto_vendido DOUBLE PRECISION NOT NULL, 
	precio_unitario DOUBLE PRECISION NOT NULL, 
	id_fecha INTEGER NOT NULL, 
	id_agente INTEGER NOT NULL, 
	id_producto INTEGER NOT NULL, 
	CONSTRAINT ventas_pkey PRIMARY KEY (ventas_id), 
	CONSTRAINT ventas_id_agente_fkey FOREIGN KEY(id_agente) REFERENCES agente (id_agente), 
	CONSTRAINT ventas_id_fecha_fkey FOREIGN KEY(id_fecha) REFERENCES fecha (id_fecha), 
	CONSTRAINT ventas_id_producto_fkey FOREIGN KEY(id_producto) REFERENCES producto (id_producto)
)

;

