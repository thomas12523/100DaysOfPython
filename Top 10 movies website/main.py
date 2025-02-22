from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float,desc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv('API_KEY')
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)

##CREATE DB
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(desc(Movie.ranking))).scalars()
    all_movies=movies.all()
    for i in range(len(all_movies)):
        all_movies[i].ranking=len(all_movies)-i
    db.session.commit()
    return render_template("index.html",movies=all_movies)

class Movie_form(FlaskForm):
    rating=StringField('Your rating Out of 10 e.g. 7.5')
    review=StringField("Your review")
    submit=SubmitField('Done')



@app.route("/edit",methods=['GET','POST'])
def edit():
    form=Movie_form()
    movie_id=request.args.get('id')
    movie_to_edit=db.get_or_404(Movie,movie_id)
    if form.validate_on_submit():
        movie_to_edit.rating=form.rating.data
        movie_to_edit.review=form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',movie=movie_to_edit,form=form)

@app.route("/delete")
def delete():
    movie_id=request.args.get('id')
    movie_to_delete=db.get_or_404(Movie,movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

class NewMovie(FlaskForm):
    title=StringField("Movie Title")
    submit=SubmitField("Add Movie")

@app.route("/add",methods=['GET','POST'])
def add():
    form=NewMovie()
    title_movie=form.title.data
    params={
        "query":title_movie,
        "include_adult":True,
        'api_key':API_KEY
    }
    movies_objects=requests.get(MOVIE_DB_SEARCH_URL,params=params).json()['results']
    if form.validate_on_submit():
        return render_template('select.html',movies=movies_objects)
    return render_template('add.html',form=form)
    
@app.route("/find")
def find():
    movie_api_id=request.args.get('id')
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": API_KEY, "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("edit", id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
