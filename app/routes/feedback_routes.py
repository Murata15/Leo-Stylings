from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Feedback

feedback = Blueprint('feedback', __name__)

@feedback.route('/submit-feedback', methods=['GET', 'POST'])
@login_required
def submit_feedback():
    if request.method == 'POST':
        message = request.form.get('message')

        fb = Feedback(
            user_id=current_user.id,
            message=message
        )
        db.session.add(fb)
        db.session.commit()

        flash('Feedback submitted!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('submit_feedback.html')

@feedback.route('/view-feedback')
@login_required
def view_feedback():
    feedbacks = Feedback.query.filter_by(user_id=current_user.id).order_by(Feedback.id.desc()).all()
    return render_template('view_feedback.html', feedbacks=feedbacks)
