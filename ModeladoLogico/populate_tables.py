import csv
from datetime import datetime
from random import choice

import orjson
from faker import Faker
from sqlalchemy import ForeignKey, MetaData, create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    declarative_base,
    mapped_column,
    sessionmaker,
)
from sqlalchemy.schema import CreateTable

DATABASE_URL = "postgresql://admin:12345@localhost:5432/bi_final"
engine = create_engine(DATABASE_URL)
DbSession = sessionmaker(bind=engine)
# session = DbSession()
Base: DeclarativeBase = declarative_base()

fake = Faker()


class Fecha(Base):
    __tablename__ = "fecha"
    id_fecha: Mapped[int] = mapped_column(primary_key=True)
    num_anio: Mapped[int] = mapped_column()
    num_mes: Mapped[int] = mapped_column()
    num_semana: Mapped[int] = mapped_column()
    num_dia: Mapped[int] = mapped_column()


class Agente(Base):
    __tablename__ = "agente"
    id_agente: Mapped[int] = mapped_column(primary_key=True)
    id_tipo_agente: Mapped[int] = mapped_column()
    nombre_tipo: Mapped[str] = mapped_column()
    nombre_agente: Mapped[str] = mapped_column()


class Efectividad(Base):
    __tablename__ = "efectividad"
    efectividad_id: Mapped[int] = mapped_column(primary_key=True)
    clientes_atendidos: Mapped[int] = mapped_column()
    unidades_vendidas: Mapped[int] = mapped_column()
    monto_vendido: Mapped[float] = mapped_column()
    precio_unitario: Mapped[float] = mapped_column()
    minutos_esperados: Mapped[int] = mapped_column()
    id_fecha: Mapped[int] = mapped_column(ForeignKey("fecha.id_fecha"))
    id_agente: Mapped[int] = mapped_column(ForeignKey("agente.id_agente"))


class Producto(Base):
    __tablename__ = "producto"
    id_producto: Mapped[int] = mapped_column(primary_key=True)
    id_division: Mapped[int] = mapped_column()
    nombre_division: Mapped[str] = mapped_column()
    nombre_producto: Mapped[str] = mapped_column()


class Ventas(Base):
    __tablename__ = "ventas"
    ventas_id: Mapped[int] = mapped_column(primary_key=True)
    unidades_vendidas: Mapped[int] = mapped_column()
    monto_vendido: Mapped[float] = mapped_column()
    precio_unitario: Mapped[float] = mapped_column()
    id_fecha: Mapped[int] = mapped_column(ForeignKey("fecha.id_fecha"))
    id_agente: Mapped[int] = mapped_column(ForeignKey("agente.id_agente"))
    id_producto: Mapped[int] = mapped_column(ForeignKey("producto.id_producto"))


class Satisfaccion(Base):
    __tablename__ = "satisfaccion"
    id_pregunta: Mapped[int] = mapped_column(primary_key=True)
    descripcion: Mapped[str] = mapped_column()
    opcion_elegida: Mapped[str] = mapped_column()


class Calidad(Base):
    __tablename__ = "calidad"
    calidad_id: Mapped[int] = mapped_column(primary_key=True)
    minutos_esperados: Mapped[int] = mapped_column()
    id_fecha: Mapped[int] = mapped_column(ForeignKey("fecha.id_fecha"))
    id_agente: Mapped[int] = mapped_column(ForeignKey("agente.id_agente"))
    id_satisfaccion: Mapped[int] = mapped_column(ForeignKey("satisfaccion.id_pregunta"))


class Retroalimentacion(Base):
    __tablename__ = "retroalimentacion"
    retroalimentacion_id: Mapped[int] = mapped_column(primary_key=True)
    clientes_atendidos: Mapped[int] = mapped_column()
    unidades_vendidas: Mapped[int] = mapped_column()
    monto_vendido: Mapped[float] = mapped_column()
    precio_unitario: Mapped[float] = mapped_column()
    minutos_esperados: Mapped[int] = mapped_column()
    id_agente: Mapped[int] = mapped_column(ForeignKey("agente.id_agente"))
    id_satisfaccion: Mapped[int] = mapped_column(ForeignKey("satisfaccion.id_pregunta"))


num_records = {
    Fecha.__tablename__: 500,
    Agente.__tablename__: 10,
    Producto.__tablename__: 15,
    Satisfaccion.__tablename__: 8,
    Efectividad.__tablename__: 250,
    Ventas.__tablename__: 500,
    Calidad.__tablename__: 400,
    Retroalimentacion.__tablename__: 350,
}

type Model = type[Fecha | Agente | Producto | Satisfaccion | Efectividad | Ventas | Calidad | Retroalimentacion]


def populate_table(
    session: Session,
    table: Model,
    *info_tables,
):
    items = [table(**fake_data(table, *info_tables)) for _ in range(num_records[table.__tablename__])]
    session.add_all(items)
    session.flush()
    return items


def fake_data(
    table: Model,
    fechas: list[Fecha] = None,
    agentes: list[Agente] = None,
    productos: list[Producto] = None,
    satisfacciones: list[Satisfaccion] = None,
):
    if table == Fecha:
        random_date = fake.date_between(start_date="-5y", end_date="-1y")
        return {
            "num_anio": random_date.year,
            "num_mes": random_date.month,
            "num_semana": random_date.isocalendar()[1],
            "num_dia": random_date.day,
        }
    if table == Agente:
        return {
            "id_tipo_agente": fake.random_number(digits=2),
            "nombre_tipo": choice(["Vendedor", "Cajero", "Gerente"]),
            "nombre_agente": fake.first_name(),
        }
    if table == Producto:
        return {
            "id_division": fake.random_number(digits=2),
            "nombre_division": choice(["Tecnología", "Muebles", "Electrodomésticos", "Hogar"]),
            "nombre_producto": choice(
                [
                    "Laptop",
                    "Smartphone",
                    "Tablet",
                    "Smartwatch",
                    "Escritorio",
                    "Silla",
                    "Mesa",
                    "Cama",
                    "Sofá",
                    "Refrigerador",
                ]
            ),
        }
    if table == Satisfaccion:
        return {
            "descripcion": choice(
                [
                    "¿Qué tan satisfecho estás con el servicio?",
                    "¿Qué tan satisfecho estás con el producto?",
                    "¿Qué tan satisfecho estás con la atención?",
                    "¿Qué tan satisfecho estás con la calidad del producto?",
                    "¿Qué tan satisfecho estás con el tiempo de espera?",
                ]
            ),
            "opcion_elegida": choice(
                [
                    "Muy satisfecho",
                    "Satisfecho",
                    "Neutral",
                    "Insatisfecho",
                    "Muy insatisfecho",
                ]
            ),
        }
    if table == Efectividad:
        return {
            "clientes_atendidos": fake.random_number(digits=3),
            "unidades_vendidas": fake.random_number(digits=3),
            "monto_vendido": fake.random_number(digits=6, fix_len=True) / 100,
            "precio_unitario": fake.random_number(digits=5) / 100,
            "minutos_esperados": fake.random_number(digits=2),
            "id_fecha": fake.random_element(elements=fechas).id_fecha,
            "id_agente": fake.random_element(elements=agentes).id_agente,
        }
    if table == Ventas:
        precio_unitario = fake.random_number(digits=5) / 100
        unidades_vendidas = fake.random_number(digits=3)
        return {
            "unidades_vendidas": unidades_vendidas,
            "monto_vendido": unidades_vendidas * precio_unitario,
            "precio_unitario": precio_unitario,
            "id_fecha": fake.random_element(elements=fechas).id_fecha,
            "id_agente": fake.random_element(elements=agentes).id_agente,
            "id_producto": fake.random_element(elements=productos).id_producto,
        }
    if table == Calidad:
        return {
            "minutos_esperados": fake.random_number(digits=2),
            "id_fecha": fake.random_element(elements=fechas).id_fecha,
            "id_agente": fake.random_element(elements=agentes).id_agente,
            "id_satisfaccion": fake.random_element(elements=satisfacciones).id_pregunta,
        }
    if table == Retroalimentacion:
        return {
            "clientes_atendidos": fake.random_number(digits=3),
            "unidades_vendidas": fake.random_number(digits=3),
            "monto_vendido": fake.random_number(digits=5),
            "precio_unitario": fake.random_number(digits=2),
            "minutos_esperados": fake.random_number(digits=2),
            "id_agente": fake.random_element(elements=agentes).id_agente,
            "id_satisfaccion": fake.random_element(elements=satisfacciones).id_pregunta,
        }


def populate_info_tables(session: Session):
    fechas = populate_table(session=session, table=Fecha)
    agentes = populate_table(session=session, table=Agente)
    productos = populate_table(session=session, table=Producto)
    satisfacciones = populate_table(session=session, table=Satisfaccion)
    return fechas, agentes, productos, satisfacciones


def populate_transaction_tables(session: Session, *info_tables):
    populate_table(session, Efectividad, *info_tables)
    populate_table(session, Ventas, *info_tables)
    populate_table(session, Calidad, *info_tables)
    populate_table(session, Retroalimentacion, *info_tables)


def populate_data():
    with DbSession() as session:
        info_tables = populate_info_tables(session)
        populate_transaction_tables(session, *info_tables)
        session.commit()


def create_modelo_fisico():
    metadata = MetaData()
    metadata.reflect(bind=engine)

    with open("ModeloFisico/create_tables.sql", "w") as f:
        for table in metadata.sorted_tables:
            create_table_sql = str(CreateTable(table).compile(engine))
            f.write(f"{create_table_sql};\n\n")


def _parse_fecha(fecha: Fecha) -> str:
    return datetime(fecha.num_anio, fecha.num_mes, fecha.num_dia).strftime("%Y-%m-%d")


def create_source_1(num_records: int):
    with DbSession() as session:
        fechas = session.scalars(select(Fecha)).all()
        agentes = session.scalars(select(Agente)).all()
        productos = session.scalars(select(Producto)).all()

        with open("ETL/ventas.csv", "w", newline="") as csvfile:
            fieldnames = [
                "Unidades Vendidas",
                "Monto Vendido",
                "Precio Unitario",
                "Fecha",
                "ID Agente",
                "ID Producto",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for _ in range(num_records):
                writer.writerow(
                    {
                        "Unidades Vendidas": fake.random_number(digits=3),
                        "Monto Vendido": fake.random_number(digits=5),
                        "Precio Unitario": fake.random_number(digits=2),
                        "Fecha": _parse_fecha(choice(fechas)),
                        "ID Agente": choice(agentes).id_agente,
                        "ID Producto": choice(productos).id_producto,
                    }
                )


def create_source_2(num_records: int):
    with DbSession() as session:
        agentes = session.scalars(select(Agente)).all()
        satisfacciones = session.scalars(select(Satisfaccion)).all()

        data = []
        for _ in range(num_records):
            data.append(
                {
                    "Clientes Atendidos": fake.random_number(digits=3),
                    "Unidades Vendidas": fake.random_number(digits=3),
                    "Monto Vendido": fake.random_number(digits=5),
                    "Precio Unitario": fake.random_number(digits=2),
                    "Minutos Esperados": fake.random_number(digits=2),
                    "ID Agente": choice(agentes).id_agente,
                    "ID Satisfaccion": choice(satisfacciones).id_pregunta,
                }
            )

        with open("ETL/retroalimentacion.json", "wb") as jsonfile:
            jsonfile.write(orjson.dumps(data, option=orjson.OPT_INDENT_2))


def init_db():
    Base.metadata.create_all(engine)
    create_modelo_fisico()


def create_sources():
    create_source_1(50)
    # create_source_2(35)


if __name__ == "__main__":
    init_db()
    # Se evita volver a poblar las tablas
    # populate_data()
    create_sources()
