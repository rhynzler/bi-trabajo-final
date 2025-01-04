-- EFECTIVIDAD

create table public.fecha
(
    id_fecha   numeric(10) not null
        constraint fecha_pk
            primary key,
    num_anio   numeric,
    num_mes    numeric,
    num_semana numeric,
    num_dia    numeric
);


create table public.agente
(
    id_agente      numeric(10) not null
        constraint agente_pk
            primary key,
    id_tipo_agente numeric,
    nombre_tipo    varchar(10),
    nombre_agente  varchar(10)

);

create table public.efectividad
(
    efectividad_id     numeric(10) not null
        constraint efectividad_pk
            primary key,
    clientes_atendidos numeric,
    unidades_vendidas  numeric,
    monto_vendido      numeric,
    precio_unitario    numeric,
    minutos_esperados  numeric,
    id_fecha           numeric(10)
        constraint fk_efectividad_r_fecha
            references fecha,
    id_agente          numeric(10)
        constraint fk_efectividad_r_agente
            references agente
);


-- VENTAS

create table public.producto
(
    id_producto     numeric(10) not null
        constraint producto_pk
            primary key,
    id_division     numeric,
    nombre_division varchar(10),
    nombre_producto varchar(10)
);

create table public.ventas
(
    ventas_id         numeric(10) not null
        constraint ventas_pk
            primary key,
    unidades_vendidas numeric,
    monto_vendido     numeric,
    precio_unitario   numeric,
    id_fecha          numeric(10)
        constraint fk_ventas_r_fecha
            references fecha,
    id_agente         numeric(10)
        constraint fk_ventas_r_agente
            references agente,
    id_producto       numeric(10)
        constraint fk_ventas_r_producto
            references producto
);

-- CALIDAD

create table public.satisfaccion
(
    id_pregunta    numeric(10) not null
        constraint satisfaccion_pk
            primary key,
    descripcion    varchar(10),
    opcion_elegida varchar(10)
);


create table public.calidad
(
    calidad_id        numeric(10) not null
        constraint calidad_pk
            primary key,
    minutos_esperados numeric,
    id_fecha          numeric(10)
        constraint fk_calidad_r_fecha
            references fecha,
    id_agente         numeric(10)
        constraint fk_calidad_r_agente
            references agente,
    id_satisfaccion   numeric(10)
        constraint fk_calidad_r_satisfaccion
            references satisfaccion
);


-- RETROALIMENTACION


create table public.retroalimentacion
(
    retroalimentacion_id     numeric(10) not null
        constraint retroalimentacion_pk
            primary key,
    clientes_atendidos numeric,
    unidades_vendidas  numeric,
    monto_vendido      numeric,
    precio_unitario    numeric,
    minutos_esperados  numeric,
    id_agente          numeric(10)
        constraint fk_retroalimentacion_r_agente
            references agente,
    id_satisfaccion    numeric(10)
        constraint fk_retroalimentacion_r_satisfaccion
            references satisfaccion
);
