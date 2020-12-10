from flask import Flask, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint
from flask import request
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    eyes = db.Column(db.Text)
    age = db.Column(db.Integer)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    __table_args__ = (PrimaryKeyConstraint('question_id', 'user_id'),)
    question_id = db.Column('question_id', db.Integer)
    user_id = db.Column('user_id', db.Integer)
    answer = db.Column(db.Text)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/form_checked', methods=['get'])
def form_checked():
    if not request.args:
        return redirect(url_for('form'))
    name = request.args.get('name')
    eyes = request.args.get('eyes')
    age = request.args.get('age')
    user = Users(
        age=age,
        eyes=eyes,
        name=name
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    tapki = request.args.get('tapki')
    meet_time = request.values.getlist('meet_time')
    alias = request.args.get('alias')
    number = request.args.get('number')
    answer1 = Answers(
        user_id=user.id,
        question_id=1,
        answer=tapki
    )
    db.session.add(answer1)
    for time in meet_time:
        answer2 = Answers(
            user_id=user.id,
            question_id=2,
            answer=time
        )
        db.session.add(answer2)
    answer3 = Answers(
        user_id=user.id,
        question_id=3,
        answer=alias
    )
    db.session.add(answer3)
    answer4 = Answers(
        user_id=user.id,
        question_id=4,
        answer=number
    )
    db.session.add(answer4)
    db.session.commit()
    return render_template('form_checked.html', user=user)


@app.route('/stats')
def stats():
    people_num = db.session.query(Users.id).count()
    avg_age = db.session.query(func.round(func.avg(Users.age), 2)).all()[0][0]
    max_age = db.session.query(func.max(Users.age)).all()[0][0s]
    tapki_yes = db.session.query(Answers).filter_by(answer='yes').count()
    tapki_per = round(tapki_yes/people_num, 2)
    nums_freq = {'684537426': 0,
                 '136247': 0,
                 '482828': 0,
                 '390175': 0
                 }
    for num in nums_freq:
        nums_freq[num] = db.session.query(Answers).filter_by(answer=num).count()
    unfreq_num = min(nums_freq, key=nums_freq.get)
    return render_template('stats.html',
                           people_num=people_num,
                           aver_age=avg_age,
                           max_age=max_age,
                           tapki_yes=tapki_yes,
                           tapki_per=tapki_per,
                           unfreq_num=unfreq_num
                           )


if __name__ == '__main__':
    app.run(debug=False)
