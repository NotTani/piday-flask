from flask import (
    Flask,
    render_template,
    request,
    abort,
    make_response
)

from db import db
from models import Score

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/leaderboard/')
def leaderboard():
    leaders = Score.query.order_by(
        Score.digits.desc()
    ).limit(25).all()
    return render_template('leaderboard.html', leaderboard=leaders)


@app.route('/play/', methods=("GET", "POST",))
def game():
    if request.method == "POST":
        print(request.form)
        digits = request.form['final_number'] or abort(400)
        name = request.form['display_name'] or abort(400)

        score = Score.query.filter_by(person=name).one_or_none()

        if not score:
            score = Score(
                person=name,
                digits=int(digits)
            )
            db.session.add(score)
        else:
            score.digits = digits

        db.session.commit()

        scores = Score.query.order_by(Score.digits.desc()).limit(50).all()

        try:
            rank = scores.index(score) + 1
        except ValueError:
            rank = -1

        resp = make_response(render_template('submitted.html', rank=rank))
        resp.set_cookie('pi_high_score', digits)
        resp.set_cookie('pi_name', name)

        return resp

    return render_template('game.html')


@app.route('/about')
def about():
    return render_template('about.html')
