from modules.config import SQLALCHEMY_DATABASE_URI, database_table_name
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import datetime


pg_engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
metadata = MetaData()
pg_base = declarative_base(pg_engine, metadata=metadata)


def get_pg_session():
    global pg_engine
    Session = sessionmaker(bind=pg_engine, expire_on_commit=True)
    session = Session()
    if not session.is_active:
        pg_engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'sslmode': 'require'}, echo=False)
        Session = sessionmaker(bind=pg_engine)
        session = Session()
    return session


"""
'action': 'input.unknown',
 'allRequiredParamsPresent': True,
 'diagnosticInfo': {'webhook_latency_ms': 199.0},
 'fulfillmentMessages': [{'text': {'text': ["I didn't quite get that. Can you "
                                            'say it again, differently?']}}],
 'fulfillmentText': "I don't quite understand. Can you possibly phrase your "
                    'question differently?',
 'intent': {'displayName': 'Default Fallback Intent',
            'isFallback': True,
            'name': 'projects/flights-e717c/agent/intents/65f3db74-38f2-4fb6-9f73-a6ff7e219d15'},
 'intentDetectionConfidence': 1.0,
 'languageCode': 'en',
 'parameters': {},
 'queryText': ' Ltoatoaga'
"""


class AnaUserQueries(pg_base):
    __tablename__ = database_table_name
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    # session_id = Column(String(256), index=True)
    user_question = Column(String(256))
    bot_response = Column(String(1024))
    bot_intent = Column(String(256))
    datetime_id = Column(DateTime, default=datetime.datetime.now)
    bot_action = Column(String(256))
    detection_confidence = Column(Integer())


metadata.create_all()


