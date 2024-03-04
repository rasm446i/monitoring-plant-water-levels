from sqlalchemy import create_engine, Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from sqlalchemy import func

DBServer = 'localhost\\SQLEXPRESS'

# Connection string
db_string = ("mssql+pyodbc://@" + DBServer + "/TestDB?driver=ODBC+Driver+17+for+SQL+Server")
engine = create_engine(db_string)

Base = declarative_base()


class MicrocontrollerInfo(Base):
    __tablename__ = 'MicrocontrollerInfo'
    microcontroller_id = Column(Integer, primary_key=True)
    placement = Column(Integer)


class MoistureData(Base):
    __tablename__ = 'MoistureData'
    id = Column(Integer, primary_key=True)
    moistlvl = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)
    microcontroller_id = Column(Integer, ForeignKey('MicrocontrollerInfo.microcontroller_id'))


Session = sessionmaker(bind=engine)  # Define Session object here


def add_new_moisture_data(id, moisturelevel):
    # laver en instans af session
    session = Session()

    microid = id
    moistlvl = moisturelevel

    # query som indsætter vores værdier
    new_moisture_entry = MoistureData(moistlvl=moistlvl, microcontroller_id=microid)

    # tilføjer query til session og commiter det
    session.add(new_moisture_entry)
    session.commit()

    #lukker session når det er comittet
    session.close()


def get_latest_moisture_data_for_all_microcontrollers():
    session = Session()

    subquery = session.query(
        MoistureData.microcontroller_id,
        func.max(MoistureData.timestamp).label('max_timestamp')
    ).group_by(MoistureData.microcontroller_id).subquery()

    query = session.query(
        MoistureData.microcontroller_id,
        MoistureData.moistlvl
    ).join(
        subquery,
        (MoistureData.microcontroller_id == subquery.c.microcontroller_id) &
        (MoistureData.timestamp == subquery.c.max_timestamp)
    )

    latest_moisture_data = query.all()

    # Funktionen ændre det hentede datasæt til et med microcontroller_id som nøgle og moistlvl som værdi.
    formatted_data = {}
    for data in latest_moisture_data:
        formatted_data[data.microcontroller_id] = data.moistlvl

    session.close()

    return formatted_data

