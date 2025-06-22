import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import Announcement
from app import db

announcement = Blueprint('announcement', __name__)

@announcement.route('/announcements')
def view_announcements():
    announcements = Announcement.query.order_by(Announcement.date_posted.desc()).all()
    return render_template('announcements.html', announcements=announcements)

@announcement.route('/admin/post-announcement', methods=['GET', 'POST'])
@login_required
def post_announcement():
    if current_user.role != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        file = request.files.get('image')

        if not title or not content or not file or file.filename == '':
            flash("All fields including image are required.", "warning")
            return redirect(url_for('announcement.post_announcement'))

        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, 'static/uploads/announcements')
        os.makedirs(upload_dir, exist_ok=True)
        image_path = os.path.join(upload_dir, filename)
        file.save(image_path)

        new_announcement = Announcement(title=title, content=content, image_filename=filename)
        db.session.add(new_announcement)
        db.session.commit()
        flash("Announcement posted successfully.", "success")
        return redirect(url_for('announcement.post_announcement'))
    
    announcements = Announcement.query.order_by(Announcement.date_posted.desc()).all()
    return render_template('admin/announcement.html', announcements=announcements)

@announcement.route('/admin/delete-announcement/<int:announcement_id>', methods=['POST'])
@login_required
def delete_announcement(announcement_id):
    if current_user.role != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('main.dashboard'))

    ann = Announcement.query.get_or_404(announcement_id)

    # Delete image file from storage
    if ann.image_filename:
        img_path = os.path.join(current_app.root_path, 'static/uploads/announcements', ann.image_filename)
        if os.path.exists(img_path):
            os.remove(img_path)

    db.session.delete(ann)
    db.session.commit()
    flash("Announcement deleted successfully.", "success")
    return redirect(url_for('announcement.post_announcement'))
