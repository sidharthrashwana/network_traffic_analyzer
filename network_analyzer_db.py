from sqlalchemy import create_engine, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.date import get_current_utc,get_today_midnight_utc
from utils.directory import create_upload_directory

Base = declarative_base()

class NetworkAnalyzer(Base):
    __tablename__ = "network"

    serial = Column("serial", Integer, primary_key=True, autoincrement=True)
    timestamp = Column("timestamp", String)
    source_mac = Column("source_mac", String)
    destination_mac = Column("destination_mac", String)
    source_ip = Column("source_ip", String)
    destination_ip = Column("destination_ip", String)
    protocol = Column("protocol", String)
    source_port = Column("source_port", String)
    destination_port = Column("destination_port", String)
    url = Column("url", String)
    length = Column("length", Integer)

    def __init__(self, timestamp, source_mac, destination_mac, 
                 source_ip, destination_ip, protocol, source_port, destination_port , 
                 url , length):
        self.timestamp = timestamp
        self.source_mac = source_mac
        self.destination_mac = destination_mac
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.protocol = protocol
        self.source_port = source_port
        self.destination_port = destination_port
        self.url = url
        self.length = length

    def __repr__(self):
        return f"""({self.timestamp}) 
                    ({self.source_mac}) 
                    ({self.destination_mac}) 
                    ({self.source_ip}) 
                    ({self.destination_ip})
                    ({self.protocol})
                    ({self.source_port})
                    ({self.destination_port})
                    ({self.url})
                    ({self.length})"""

def insert_to_db(obj):
    """
        To insert one object at a time.
        Ex:
            {}
    """
    session.add(obj)
    session.commit()

def insert_to_db_all(objs):
    """
        To insert all list of objects at once.
        Ex:
            [{},{}...]
    """
    session.add_all(objs)
    session.commit()

today_timestamp = get_today_midnight_utc()
existing_main_dir = create_upload_directory("db")
if existing_main_dir:
    upload_path = f"db/{today_timestamp}"
    existing_sub_dir = create_upload_directory(upload_path)
    if existing_sub_dir:
        current_timestamp = get_current_utc()
        file_path = f"db/{today_timestamp}/network_history_{current_timestamp}.db"
        url = f"sqlite:///{file_path}"
        engine = create_engine(url, echo=True)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()