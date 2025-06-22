from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Service

service_bp = Blueprint('service', __name__)

@service_bp.route('/services')
@login_required
def service_directory():
    department = request.args.get('department')
    if department:
        services = Service.query.filter_by(department=department).all()
    else:
        services = Service.query.all()
    departments = db.session.query(Service.department).distinct()
    return render_template('services.html', services=services, departments=departments)

@service_bp.route('/services/<int:service_id>')
@login_required
def service_detail(service_id):
    service = Service.query.get_or_404(service_id)
    return render_template('service_detail.html', service=service)

@service_bp.route('/admin/add-service', methods=['GET', 'POST'])
@login_required
def add_service():
    if current_user.role != 'admin':
        flash("Access denied.", "danger")
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        title = request.form['title']
        department = request.form['department']
        description = request.form['description']
        requirements = request.form['requirements']
        steps = request.form['steps']

        new_service = Service(
            title=title,
            department=department,
            description=description,
            requirements=requirements,
            steps=steps
        )
        db.session.add(new_service)
        db.session.commit()
        flash("Service added successfully.", "success")
        return redirect(url_for('service.service_directory'))

    return render_template('admin/add_service.html')
