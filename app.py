#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from models import Venue, Show, Artist, db
from datetime import datetime


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)

#db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues -DONE
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  info = db.session.query(Venue.city, Venue.state)

  for x in info:
    venues = Venue.query.filter(Venue.city==x.city).filter(Venue.state==x.state).all()
    data.append({'city': x.city, 'state': x.state, 'venues': venues})
    print(data)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form['search_term']
  venues = Venue.query.filter(Venue.name.ilike('%{}%'.format(request.form['search_term'])))
  response = {}
  response['data'] = venues
  response['count'] = venues.count()
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id=venue_id).all()
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()

  for show in shows:
    showData = {
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      "artist_image_link": show.artist.image_link,
      'start_time': str(show.start_time)
    }
    
    if show.start_time > current_time:
      upcoming_shows.append(showData)
    else:
      past_shows.append(showData)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "facebook_link": venue.facebook_link,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue -DONE
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form['genres']
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website_link']
    seeking_talent = True if request.form['seeking_talent'] == 'y' else False
    seeking_description = request.form['seeking_description']
    
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone,
    genres=genres, image_link=image_link, facebook_link=facebook_link, website=website,
    seeking_talent=seeking_talent, seeking_description=seeking_description)

    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!') 

  except Exception as e:
    error = True
    db.session.rollback()
    flash('Venue ' + request.form['name'] + ' could not be listed.')
    print(e)

  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  try:
    deletedVenue = Venue.query.get(venue_id)
    db.session.delete(deletedVenue)
    db.session.commit()
    flash('Venue ' + deletedVenue.name + ' has been deleted!')
  except Exception as e:
    error = True
    db.session.rollback()
    flash('Venue ' + delete_venue.name + ' could not be deleted.')
    print(e)
  finally:
    db.session.close()      


#  Artists -DONE
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = db.session.query(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form['search_term']
  artists = Artist.query.filter(Artist.name.ilike('%{}%'.format(request.form['search_term'])))
  response = {}
  response['data'] = artists
  response['count'] = artists.count()
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  shows = Show.query.filter_by(artist_id=artist_id).all()
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()

  for show in shows:
    showData = {
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'venue_image_link': show.venue.image_link,
      'start_time': str(show.start_time)
    }
    
    if show.start_time > current_time:
      upcoming_shows.append(showData)
    else:
      past_shows.append(showData)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update -DONE
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  artist_data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website_link": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venues,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.facebook_link = request.form['facebook_link']
    artist.genres = request.form['genres']
    artist.image_link = request.form['image_link']
    artist.website = request.form['website_link']

    flash('Updating ' + artist.name + ' succeeded')
    db.session.commit()

  except Exception as e:
    db.session.rollback()
    flash('Updating ' + artist.name + ' has failed.')
    print(e)

  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  venue_data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "facebook_link": venue.facebook_link,
    "image_link": venue.image_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.facebook_link = request.form['facebook_link']
    venue.genres = request.form['genres']
    venue.image_link = request.form['image_link']
    venue.website = request.form['website_link']

    flash('Updating ' + venue.name + ' succeeded')
    db.session.commit()

  except Exception as e:
    db.session.rollback()
    flash('Updating ' + venue.name + ' has failed.')
    print(e)

  finally:
    db.session.close() 
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist #DONE
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form['genres']
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website_link']
    seeking_venue = True if request.form['seeking_venue'] == 'y' else False
    seeking_description = request.form['seeking_description']
    
    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link,
    facebook_link=facebook_link, website=website,
    seeking_venues=seeking_venue, seeking_description=seeking_description)

    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except Exception as e:
    error = True
    db.session.rollback()
    flash('Artist ' + request.form['name'] + ' could not be listed.')
    print(e)

  finally:
    db.session.close()
  return render_template('pages/home.html')

#  Shows -DONE
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.all()
  data = []
  for show in shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": str(show.start_time)
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
    venue_id = request.form['venue_id']
    artist_id = request.form['artist_id']
    start_time = request.form['start_time']

    show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)

    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    error = True
    db.session.rollback()
    flash('Show could not be listed.')
    print(sys.exc_info())
  finally:    
    db.session.close()
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
