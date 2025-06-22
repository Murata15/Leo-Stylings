from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file, jsonify
from flask_login import login_required, current_user
from app.models import DocumentRequest
from app import db
from sqlalchemy import or_, and_
from io import BytesIO
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from datetime import datetime

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    status = request.args.get('status')
    doc_type = request.args.get('document_type')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    tracking = request.args.get('tracking')

    query = DocumentRequest.query

    if tracking:
        query = query.filter(DocumentRequest.tracking_number.like(f"%{tracking}%"))
    if status:
        query = query.filter_by(status=status)
    if doc_type:
        query = query.filter_by(document_type=doc_type)
    if from_date and to_date:
        try:
            start = datetime.strptime(from_date, '%Y-%m-%d')
            end = datetime.strptime(to_date, '%Y-%m-%d')
            query = query.filter(DocumentRequest.date_requested.between(start, end))
        except:
            flash("Invalid date format", "warning")

    requests = query.order_by(DocumentRequest.date_requested.desc()).all()
    return render_template('admin_dashboard.html', requests=requests)


@admin.route('/admin/update-status/<int:request_id>', methods=['POST'])
@login_required
def update_status(request_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    new_status = request.form.get('status')
    req = DocumentRequest.query.get_or_404(request_id)
    req.status = new_status
    db.session.commit()
    flash('Status updated.', 'success')
    return redirect(url_for('admin.admin_dashboard'))


@admin.route('/admin/export/excel')
@login_required
def export_excel():
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))

    requests = DocumentRequest.query.all()
    data = [{
        "Tracking": r.tracking_number,
        "User ID": r.user_id,
        "Type": r.document_type,
        "Purpose": r.purpose,
        "Status": r.status,
        "Requested On": r.date_requested.strftime('%Y-%m-%d')
    } for r in requests]

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Requests')

    output.seek(0)
    return send_file(output, download_name="document_requests.xlsx", as_attachment=True)


@admin.route('/admin/export/pdf')
@login_required
def export_pdf():
    if current_user.role != 'admin':
        return redirect(url_for('main.dashboard'))

    requests = DocumentRequest.query.all()
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    table_data = [["Tracking", "User ID", "Type", "Purpose", "Status", "Requested On"]]

    for r in requests:
        table_data.append([
            r.tracking_number, r.user_id, r.document_type,
            r.purpose, r.status, r.date_requested.strftime('%Y-%m-%d')
        ])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ]))

    doc.build([table])
    buffer.seek(0)
    return send_file(buffer, download_name="document_requests.pdf", as_attachment=True)
