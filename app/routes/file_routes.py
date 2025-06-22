from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, flash
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

file_routes = Blueprint('file_routes', __name__)

UPLOAD_FOLDER = 'app/static/downloads'

@file_routes.route('/downloadable-forms')
def downloadable_forms():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('downloadable_forms.html', files=files)

@file_routes.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@file_routes.route('/admin/forms', methods=['GET', 'POST'])
@login_required
def manage_forms():
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename:
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash("File uploaded successfully", "success")
            return redirect(url_for('file_routes.manage_forms'))
        else:
            flash("No file selected", "warning")

    files = os.listdir(UPLOAD_FOLDER)
    return render_template('admin/manage_forms.html', files=files)

@file_routes.route('/admin/forms/delete/<filename>', methods=['POST'])
@login_required
def delete_file(filename):
    if current_user.role != 'admin':
        flash("Access denied", "danger")
        return redirect(url_for('main.dashboard'))

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f"{filename} deleted.", "success")
    else:
        flash("File not found.", "warning")
    return redirect(url_for('file_routes.manage_forms'))
