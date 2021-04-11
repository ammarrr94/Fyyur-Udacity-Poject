from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(50)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(200))
    venue_show = db.relationship('Show', backref='venue', lazy="joined")

    def __repr__(self):
        return f'<Venue: {self.id} name: {self.name}>'


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(50)))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    seeking_venues = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(200))
    artist_show = db.relationship('Show', backref='artist', lazy="joined")

    def __repr__(self):
        return f'<Artist: {self.id} name: {self.name}>'


class Show(db.Model):
  __tablename__ = 'Show'

  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False, primary_key=True)
  
  def __repr__(self):
      return f'<Show: {self.id} {self.start_time}, artist_id: {self.artist_id}, Venue_id: {self.venue_id}>'