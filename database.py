from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgres://gttgpzvugpdhlx:6gGnyBfNOIY5DEYU5w2a1v9oRM@ec2-54-195-248-72.eu-west-1.compute.amazonaws.com:5432/da02oviphgjjm0', convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=True,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models.Model
    Base.metadata.create_all(bind=engine)
