from faker import Faker
from sqlalchemy import ForeignKey, Integer, create_engine, Column, Numeric, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session, declarative_base

DATABASE_URL = "postgresql://admin:12345@localhost:5432/bi_final"
engine = create_engine(DATABASE_URL)
DbSession = sessionmaker(bind=engine)
# session = DbSession()
Base: DeclarativeBase = declarative_base()

fake = Faker()


class Fecha(Base):
    __tablename__ = "fecha"
    id_fecha = Column(Integer, primary_key=True)
    num_anio = Column(Numeric)
    num_mes = Column(Numeric)
    num_semana = Column(Numeric)
    num_dia = Column(Numeric)


class Agente(Base):
    __tablename__ = "agente"
    id_agente = Column(Integer, primary_key=True)
    id_tipo_agente = Column(Numeric)
    nombre_tipo = Column(String)
    nombre_agente = Column(String)


class Efectividad(Base):
    __tablename__ = "efectividad"
    efectividad_id = Column(Integer, primary_key=True)
    clientes_atendidos = Column(Numeric)
    unidades_vendidas = Column(Numeric)
    monto_vendido = Column(Numeric)
    precio_unitario = Column(Numeric)
    minutos_esperados = Column(Numeric)
    id_fecha = Column(ForeignKey("fecha.id_fecha"))
    id_agente = Column(ForeignKey("agente.id_agente"))


class Producto(Base):
    __tablename__ = "producto"
    id_producto = Column(Integer, primary_key=True)
    id_division = Column(Numeric)
    nombre_division = Column(String)
    nombre_producto = Column(String)


class Ventas(Base):
    __tablename__ = "ventas"
    ventas_id = Column(Integer, primary_key=True)
    unidades_vendidas = Column(Numeric)
    monto_vendido = Column(Numeric)
    precio_unitario = Column(Numeric)
    id_fecha = Column(ForeignKey("fecha.id_fecha"))
    id_agente = Column(ForeignKey("agente.id_agente"))
    id_producto = Column(ForeignKey("producto.id_producto"))


class Satisfaccion(Base):
    __tablename__ = "satisfaccion"
    id_pregunta = Column(Integer, primary_key=True)
    descripcion = Column(String)
    opcion_elegida = Column(String)


class Calidad(Base):
    __tablename__ = "calidad"
    calidad_id = Column(Integer, primary_key=True)
    minutos_esperados = Column(Numeric)
    id_fecha = Column(ForeignKey("fecha.id_fecha"))
    id_agente = Column(ForeignKey("agente.id_agente"))
    id_satisfaccion = Column(ForeignKey("satisfaccion.id_pregunta"))


class Retroalimentacion(Base):
    __tablename__ = "retroalimentacion"
    retroalimentacion_id = Column(Integer, primary_key=True)
    clientes_atendidos = Column(Numeric)
    unidades_vendidas = Column(Numeric)
    monto_vendido = Column(Numeric)
    precio_unitario = Column(Numeric)
    minutos_esperados = Column(Numeric)
    id_agente = Column(ForeignKey("agente.id_agente"))
    id_satisfaccion = Column(ForeignKey("satisfaccion.id_pregunta"))


num_records = {
    Fecha.__tablename__: 100,
    Agente.__tablename__: 10,
    Producto.__tablename__: 15,
    Satisfaccion.__tablename__: 8,
    Efectividad.__tablename__: 250,
    Ventas.__tablename__: 500,
    Calidad.__tablename__: 400,
    Retroalimentacion.__tablename__: 350,
}

type Model = type[
    Fecha
    | Agente
    | Producto
    | Satisfaccion
    | Efectividad
    | Ventas
    | Calidad
    | Retroalimentacion
]


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
        return {
            "num_anio": fake.year(),
            "num_mes": fake.month(),
            "num_semana": fake.random_int(min=1, max=52),
            "num_dia": fake.day_of_month(),
        }
    if table == Agente:
        return {
            "id_tipo_agente": fake.random_number(digits=2),
            "nombre_tipo": fake.word(),
            "nombre_agente": fake.first_name(),
        }
    if table == Producto:
        return {
            "id_division": fake.random_number(digits=2),
            "nombre_division": fake.word(),
            "nombre_producto": fake.word(),
        }
    if table == Satisfaccion:
        return {
            "descripcion": fake.word(),
            "opcion_elegida": fake.word(),
        }
    if table == Efectividad:
        return {
            "clientes_atendidos": fake.random_number(digits=3),
            "unidades_vendidas": fake.random_number(digits=3),
            "monto_vendido": fake.random_number(digits=5),
            "precio_unitario": fake.random_number(digits=2),
            "minutos_esperados": fake.random_number(digits=2),
            "id_fecha": fake.random_element(elements=fechas).id_fecha,
            "id_agente": fake.random_element(elements=agentes).id_agente,
        }
    if table == Ventas:
        return {
            "unidades_vendidas": fake.random_number(digits=3),
            "monto_vendido": fake.random_number(digits=5),
            "precio_unitario": fake.random_number(digits=2),
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


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    populate_data()
