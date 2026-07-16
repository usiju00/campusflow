from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.wallet import bp
from app.models import Wallet, Transaction
from app import db
from datetime import datetime
import uuid

@bp.route('/wallet')
@login_required
def wallet():
    return render_template('wallet/wallet.html', student=current_user)

@bp.route('/topup', methods=['GET', 'POST'])
@login_required
def topup():
    if request.method == 'POST':
        from decimal import Decimal
        amount = Decimal(request.form['amount'])
        wallet = current_user.wallet
        wallet.balance += amount
        wallet.updated_at = datetime.utcnow()
        transaction = Transaction(
            wallet_id=wallet.id,
            transaction_type='credit',
            amount=amount,
            reference=str(uuid.uuid4())[:8].upper(),
            description='Wallet top-up'
        )
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('wallet.wallet'))
    return render_template('wallet/topup.html')
