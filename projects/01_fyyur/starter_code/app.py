# Notes: 
# - Add stuff for updating venues
# - buttones for deleting/editing artists
# - buttons for deleting/editing venues
# - buttons for deleteing/editing shows

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

from models import *

#----------------------------------------------------------------------------#
# Filters
#----------------------------------------------------------------------------#

def format_datetime(date, format='medium'):
  if isinstance(date, str):
      date = dateutil.parser.parse(date)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  ----------------------------------------------------------------
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = City.query.all()
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term=request.form.get('search_term', '')
  results = SearchResults(Venue.query.filter(func.lower(Venue.name).contains(search_term.lower())).all())
  return render_template('pages/search_venues.html', results=results, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
  data = Venue.query.get(venue_id)
  if data.shows:
    data.past_shows = [show for show in data.shows if show.start_time < datetime.now()]
    data.past_shows_count = len(data.past_shows)
    data.upcoming_shows = [show for show in data.shows if show.start_time > datetime.now()]
    data.upcoming_shows_count = len(data.upcoming_shows)
  else:
    data.past_shows = []
    data.past_shows_count = 0
    data.upcoming_shows = []
    data.upcoming_shows_count = 0 
  
  return render_template('pages/show_venue.html', venue=data)

#  ----------------------------------------------------------------
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  new_venue = Venue(name=request.form.get('name'))
  new_venue.city = City.get_unique(
      city=request.form.get('city'),
      state = request.form.get('state')
  )
  new_venue.address = request.form.get('address', '')
  new_venue.phone = request.form.get('phone', '')
  new_venue.genres = [Genre.get_unique(name=genre) for genre in request.form.getlist('genres')]
  new_venue.facebook_link = request.form.get('facebook_link')

  try:
      db.session.add(new_venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except: 
  # DONE: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + new_venue.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  venue = Venue.query.get(venue_id)
  try:
    db.session.delete(venue)
    db.session.commit()
    flash('Venue '+ venue.name + ' was successfully deleted.')
  except:
    flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  ----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  results = SearchResults(Artist.query.filter(func.lower(Artist.name).contains(search_term.lower())).all())
  return render_template('pages/search_artists.html', results=results, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: replace with real venue data from the venues table, using venue_id
  data = Artist.query.get(artist_id)
  if data.shows:
    data.past_shows = [show for show in data.shows if show.start_time < datetime.now()]
    data.past_shows_count = len(data.past_shows)
    data.upcoming_shows = [show for show in data.shows if show.start_time > datetime.now()]
    data.upcoming_shows_count = len(data.upcoming_shows)
  else:
    data.past_shows = []
    data.past_shows_count = 0
    data.upcoming_shows = []
    data.upcoming_shows_count = 0 
   
  return render_template('pages/show_artist.html', artist=data)
  

#  ----------------------------------------------------------------
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city.city
  form.state.data = artist.city.state
  form.phone.data = artist.phone
  form.genres.data = ['Alternative', 'Classical'] #[genre.name for genre in artist.genres]
  form.facebook_link.data = artist.facebook_link
  # DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  artist.name = request.form.get('name')
  artist.city = City.get_unique(
      city=request.form.get('city'),
      state=request.form.get('state')
  )
  artist.phone = request.form.get('phone')
  artist.genres = [Genre.get_unique(name=genre) for genre in request.form.getlist('genres')]
  artist.facebook_link = request.form.get('facebook_link')
  db.session.add(artist)
  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.genres.data = venue.genres
  form.address.data = venue.address
  form.city.data = venue.city.city
  form.state.data = venue.city.state
  form.phone.data = venue.phone
  form.image_link.data = venue.image_link
  form.facebook_link.data = venue.facebook_link
  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  venue.name = request.form.get('name')
  venue.genres = [Genre.get_unique(genre) for genre in request.form.getlist('genres')]
  venue.address = request.form.get('address')
  venue.city = City.get_unique(
      city = request.form.get('city'),
      state = request.form.get('state')
  )
  venue.phone = request.form.get('phone')
  venue.facebook_link = request.form.get('facebook_link')
  db.session.add(venue)
  db.session.commit()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  ----------------------------------------------------------------
#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  new_artist = Artist(name=request.form.get('name'))
  new_artist.city = City.get_unique(
    city=request.form.get('city'),
    state=request.form.get('state')
  )
  new_artist.phone = request.form.get('phone')
  new_artist.genres = [
    Genre.get_unique(name=genre) for genre in request.form.getlist('genres')
  ]
  new_artist.facebook_link = request.form.get('facebook_link')

  # on successful db insert, flash success
  try:
    db.session.add(new_artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # DONE: on unsuccessful db insert, flash an error instead.
  except:
    flash('An error occurred. Artist ' + new_artist.name + ' could not be listed.')
  return render_template('pages/home.html')


#  ----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = Show.query.order_by(Show.start_time).all()
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
  new_show = Show(
    artist_id=request.form.get('artist_id'),
    venue_id=request.form.get('venue_id'),
    start_time=request.form.get('start_time')
  )
  # on successful db insert, flash success
  try:
    db.session.add(new_show)
    db.session.commit()
    flash('Show was successfully listed!')
  # DONE: on unsuccessful db insert, flash an error instead.
  except:
    flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
