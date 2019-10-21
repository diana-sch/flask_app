import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from werkzeug.exceptions import abort

from flaskr.auth import login_required
import requests

bp = Blueprint('jazda', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    jazdy = db.execute(
        'SELECT j.id, start, ciel, trvanie, driver_id, username'
        ' FROM jazda j JOIN user u ON j.driver_id = u.id'
    ).fetchall()
    # stops = get_stops()
    return render_template('jazda/moje_jazdy.html', jazdy=jazdy)


@bp.route('/pridat_jazdu', methods=('GET', 'POST'))
@login_required
def pridat_jazdu():
    if request.method == 'POST':
        start = request.form['start']
        ciel = request.form['ciel']
        trvanie = request.form['trvanie']
        error = None

        if not start:
            error = 'start is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO jazda (start, ciel, trvanie, driver_id)'
                'VALUES (?, ?, ?, ?)',
                (start, ciel, trvanie, g.user['id'])
            )
            db.commit()
            return redirect(url_for('jazda.index'))
    stops = get_stops()
    return render_template('jazda/pridat_jazdu.html', stops=stops)


def get_stops():
    data = requests.post('https://gate.slovnaftbajk.sk/AppGate2.php', json={"Cmd": "GetAllStationInfo", "Area": "BA"})
    # pprint.pprint(data.json())
    json_obj = data.json()
    names = []
    for piece in json_obj['Info']:
        name = str([piece['Name']])
        names.append(name)
    return names

# momo = get_stops()
# print(momo[0])





