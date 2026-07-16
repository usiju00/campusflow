from flask import render_template, send_file
from flask_login import login_required, current_user
from app.identity import bp
import jwt
import qrcode
import io
import os
from datetime import datetime

@bp.route('/identity')
@login_required
def identity():
    return render_template('identity/identity.html', student=current_user)

@bp.route('/qrcode')
@login_required
def generate_qr():
    payload = {
        'matric_number': current_user.matric_number,
        'full_name': current_user.full_name,
        'department': current_user.department,
        'level': current_user.level,
        'issued': str(datetime.utcnow())
    }
    token = jwt.encode(payload, 'campusflow-secret', algorithm='HS256')
    qr = qrcode.make(token)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

