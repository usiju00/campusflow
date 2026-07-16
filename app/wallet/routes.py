from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.wallet import bp
from app.models import Wallet, Transaction
from app import db
from datetime import datetime
from decimal import Decimal
import uuid

@bp.route('/wallet')
@login_required
def wallet():
    return render_template('wallet/wallet.html', student=current_user)

@bp.route('/topup', methods=['GET', 'POST'])
@login_required
def topup():
    if request.method == 'POST':
        amount = Decimal(request.form['amount'])
        w = current_user.wallet
        w.balance += amount
        w.updated_at = datetime.utcnow()
        txn = Transaction(
            wallet_id=w.id,
            transaction_type='credit',
            amount=amount,
            reference=str(uuid.uuid4())[:8].upper(),
            description='Wallet top-up'
        )
        db.session.add(txn)
        db.session.commit()
        return redirect(url_for('wallet.wallet'))
    return render_template('wallet/topup.html')

@bp.route('/transactions')
@login_required
def transactions():
    w = current_user.wallet
    txns = Transaction.query.filter_by(
        wallet_id=w.id
    ).order_by(Transaction.created_at.desc()).all()
    return render_template('wallet/transactions.html', transactions=txns)
