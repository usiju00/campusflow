from flask import render_template
from flask_login import login_required, current_user
from app.admin import bp
from app.models import Student, Transaction, Wallet
from app import db

@bp.route('/admin')
@login_required
def dashboard():
    if not current_user.is_admin:
        return 'Access denied', 403
    total_students = Student.query.count()
    total_transactions = Transaction.query.count()
    total_balance = db.session.query(
        db.func.sum(Wallet.balance)
    ).scalar() or 0
    recent = Transaction.query.order_by(
        Transaction.created_at.desc()
    ).limit(10).all()
    return render_template('admin/dashboard.html',
        total_students=total_students,
        total_transactions=total_transactions,
        total_balance=total_balance,
        recent=recent
    )
