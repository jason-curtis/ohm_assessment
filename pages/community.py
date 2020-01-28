from collections import OrderedDict

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

def _get_recently_enrolled_users_with_phone():
    ''' Jason note: I Kept this more complex one separate from the simpler one for the purposes of the exercise.
    I came back to this extra-credit feature at the end
    and did a very quick pass at it, so it's very much not polished.
    I would like to double check that the sql can't be simpler or more efficient,
    and also think about whether the in-python manipulation could be made more straightforward.
    '''
    rows = db.engine.execute('''
    SELECT u.user_id, display_name, tier, point_balance, attribute AS phone FROM
        (
            SELECT user_id, display_name, tier, signup_date, point_balance
            FROM user
            ORDER BY signup_date DESC
            LIMIT 5
        ) AS u
        LEFT JOIN
        (
            SELECT user_id, attribute
            FROM rel_user_multi
            WHERE rel_lookup = 'PHONE'
        ) AS r
        ON u.user_id = r.user_id
    ''')
    users_by_id = OrderedDict()

    for row in rows:
        if row.user_id in users_by_id:
            users_by_id[row.user_id]['phone_numbers'].append(row.phone)
        else:
            row_dict = {
                'user_id': row.user_id,
                'display_name': row.display_name,
                'tier': row.tier,
                'point_balance': row.point_balance
            }
            row_dict['phone_numbers'] = [row.phone] if row.phone else []
            users_by_id[row.user_id] = row_dict

    return list(users_by_id.values())


@app.route('/community', methods=['GET'])
def community():
    login_user(User.query.get(1))

    args = {
        'recently_enrolled_users': _get_recently_enrolled_users(),
        'recently_enrolled_users_with_phone': _get_recently_enrolled_users_with_phone(),
    }
    return render_template("community.html", **args)

