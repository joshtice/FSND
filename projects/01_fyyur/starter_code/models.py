from app import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

genre_venues = db.Table('genre_venues',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True)
)
genre_artists = db.Table('genre_artists',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)
)


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f"<Venue name='{self.name}'>"


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(120))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f"<Artist name='{self.name}'>"


class City(db.Model):
    __tablename__ = 'city'
    __table_args__ = (
        db.UniqueConstraint('city', 'state', name='unique_city_state'),
    )

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    venues = db.relationship('Venue', backref='city', lazy=True)
    artists = db.relationship('Artist', backref='city', lazy=True)

    def __repr__(self):
        return f"<City city='{self.city}'>"


class Genre(db.Model):
  __tablename__ = 'genre'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), unique=True)
  venues = db.relationship('Venue', secondary=genre_venues,
      backref=db.backref('genres', lazy=True))
  artists = db.relationship('Artist', secondary=genre_artists,
      backref=db.backref('genres', lazy=True))

  def __repr__(self):
      return f"<Genre name='{self.name}'>"


class Show(db.Model):
    __tablename__ = 'show'
    __table_args__ = (
        db.UniqueConstraint('artist_id', 'start_time', name='unique_start_time'),
    )

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    start_time = db.Column(db.DateTime)


class SearchResults:

    def __init__(self, data=[]):
        self.data = data
        self.count = len(data)

