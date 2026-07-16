from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.wallet import bp
from app.models import Wallet, Transaction, Student
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

@bp.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'POST':
        matric_number = request.form['matric_number']
        amount = Decimal(request.form['amount'])
        recipient = Student.query.filter_by(matric_number=matric_number).first()
        if not recipient:
            return render_template('wallet/transfer.html', error='Student not found')
        if current_user.wallet.balance < amount:
            return render_template('wallet/transfer.html', error='Insufficient balance')
        debit = Transaction(
            wallet_id=current_user.wallet.id,
            transaction_type='debit',
            amount=amount,
            reference=str(uuid.uuid4())[:8].upper(),
            description='Transfer to ' + recipient.matric_number
        )
        credit = Transaction(
            wallet_id=recipient.wallet.id,
            transaction_type='credit',
            amount=amount,
            reference=str(uuid.uuid4())[:8].upper(),
            description='Transfer from ' + current_user.matric_number
        )
        current_user.wallet.balance -= amount
        recipient.wallet.balance += amount
        db.session.add(debit)
        db.session.add(credit)
        db.session.commit()
        return redirect(url_for('wallet.wallet'))
    return render_template('wallet/transfer.html', error=None)
