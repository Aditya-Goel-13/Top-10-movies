from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
from check import search_movie

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)

# CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)


class Add(FlaskForm):
    name = StringField("Movie title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


# Movie rating form
class RatingForm(FlaskForm):
    rate = FloatField("Your Rating Out Of 10 e.g. 7.3", validators=[DataRequired(), NumberRange(min=0, max=10)])
    review = StringField(label="Your review", validators=[DataRequired()])
    submit = SubmitField("Submit")


# CREATE TABLE
class Movie(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    title = db.Column(String, unique=True, nullable=False)
    year = db.Column(String, nullable=False)
    description = db.Column(String, nullable=False)
    rating = db.Column(Float)
    ranking = db.Column(Integer)
    review = db.Column(String)
    img_url = db.Column(String, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()

# with app.app_context():
#     new_movie = Movie(
#         title="Avatar The Way of Water",
#         year=2022,
#         description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#         img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
#     )
#
#     db.session.add(new_movie)
#     db.session.commit()
#

@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movie = result.scalars().all()
    for i in range(len(all_movie)):
        all_movie[i].ranking = len(all_movie)-i
    db.session.commit()

    return render_template("index.html", movies=all_movie)


@app.route('/edit/<string:title>', methods=['POST', 'GET'])
def edit(title: str):
    form = RatingForm()
    curr = Movie.query.filter_by(title=title).first()

    if form.validate_on_submit():
        curr.rating = form.rate.data
        curr.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, title=curr.title)


@app.route("/delete/<int:id>")
def delete(id: int):
    curr = Movie.query.filter_by(id=id).first()
    db.session.delete(curr)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=["POST", "GET"])
def add():
    form = Add()
    if form.validate_on_submit():
        return redirect(url_for('select', name=form.name.data))
    return render_template('add.html', form=form)


@app.route("/select/<name>")
def select(name):
    lom = search_movie(name)
    return render_template("select.html", lom=lom)


@app.route("/add_data")
def add_data():
    with app.app_context():
        new_movie = Movie(
            title=request.args.get('name'),
            year=request.args.get('year'),
            description=request.args.get('des'),
            img_url=request.args.get('url')
        )

        db.session.add(new_movie)
        db.session.commit()

    return redirect(url_for('edit', title=request.args.get('name')))

if __name__ == '__main__':
    app.run(debug=True)
