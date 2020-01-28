from flask import jsonify, render_template, request, Response
from flask.ext.login import current_user, login_user

from functions import app
from models import User, db


def _get_recently_enrolled_users():
    return db.engine.execute('''
    select display_name, tier, point_balance from user
        ORDER BY signup_date DESC
        LIMIT 5
    ''')

@app.route('/community', methods=['GET'])
def community():
    login_user(User.query.get(1))

    args = {
        'recently_enrolled_users': _get_recently_enrolled_users(),
    }
    return render_template("community.html", **args)

