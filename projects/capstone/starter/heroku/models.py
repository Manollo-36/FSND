
import os
from sqlalchemy import Column, String,Integer,DateTime
from flask_sqlalchemy import SQLAlchemy
import json
env = os.environ
print (env)
database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    print(database_path)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Actors(db.Model):  
  __tablename__ = 'Actors'

  id = Column(Integer, primary_key=True)
  name = Column(String,nullable=False)
  age = Column(Integer,nullable=False)
  gender = Column(String,nullable=False)
 

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date}
  
class Movies(db.Model):  
    __tablename__ = 'Movies'
    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)
    release_date = Column(DateTime,nullable=True)
    duration = Column(Integer, nullable=False)
    imdb_rating = Column(Integer, nullable=False)
    cast = db.relationship('Actor',backref='movies', lazy='joined',cascade='all,delete')

    def __init__(self, name, age,gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender':self.gender}
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()  

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())