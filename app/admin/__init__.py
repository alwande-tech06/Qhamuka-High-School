import os
import uuid

from flask import (Blueprint, render_template, redirect, url_for, flash,
                   current_app, request, abort)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.models import db, Announcement, Gallery, ContactSubmission, MatricResult, ApplicationRequest
from app.forms import AnnouncementForm, GalleryUploadForm, MatricResultForm

admin = Blueprint('admin', __name__)


@admin.route('/')
@admin.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_notices': Announcement.query.count(),
        'media_uploads': Gallery.query.count(),
        'unread_messages': ContactSubmission.query.filter_by(is_read=False).count(),
    }
    recent_activity = (Announcement.query
                       .order_by(Announcement.date_posted.desc())
                       .limit(5)
                       .all())
    return render_template('admin/dashboard.html', stats=stats,
                           recent_activity=recent_activity)


@admin.route('/announcements', methods=['GET', 'POST'])
@login_required
def announcements():
    form = AnnouncementForm()
    if form.validate_on_submit():
        post = Announcement(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_published=form.is_published.data,
            created_by=current_user.user_id,
        )
        db.session.add(post)
        db.session.commit()
        flash('Announcement saved.', 'success')
        return redirect(url_for('admin.announcements'))

    all_posts = Announcement.query.order_by(Announcement.date_posted.desc()).all()
    return render_template('admin/announcements.html', form=form,
                           announcements=all_posts)


@admin.route('/announcements/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_announcement(post_id):
    post = Announcement.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Announcement deleted.', 'success')
    return redirect(url_for('admin.announcements'))


@admin.route('/gallery', methods=['GET', 'POST'])
@login_required
def gallery():
    form = GalleryUploadForm()
    if form.validate_on_submit():
        file = form.image.data
        # Unique, safe filename
        ext = secure_filename(file.filename).rsplit('.', 1)[-1].lower()
        filename = f'{uuid.uuid4().hex}.{ext}'
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        item = Gallery(
            image_path=f'uploads/{filename}',  # relative to static/
            caption=form.caption.data,
            event_name=form.event_name.data,
            uploaded_by=current_user.user_id,
        )
        db.session.add(item)
        db.session.commit()
        flash('Image uploaded to the gallery.', 'success')
        return redirect(url_for('admin.gallery'))

    photos = Gallery.query.order_by(Gallery.date_uploaded.desc()).all()
    return render_template('admin/gallery_mgmt.html', form=form, photos=photos)


@admin.route('/gallery/<int:image_id>/delete', methods=['POST'])
@login_required
def delete_image(image_id):
    item = Gallery.query.get_or_404(image_id)
    # Remove the file from disk if present
    file_path = os.path.join(current_app.root_path, 'static', item.image_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(item)
    db.session.commit()
    flash('Image removed.', 'success')
    return redirect(url_for('admin.gallery'))


@admin.route('/submissions')
@login_required
def submissions():
    messages = (ContactSubmission.query
                .order_by(ContactSubmission.submitted_at.desc())
                .all())
    unread_count = ContactSubmission.query.filter_by(is_read=False).count()

    selected = None
    selected_id = request.args.get('selected', type=int)
    if selected_id:
        selected = ContactSubmission.query.get_or_404(selected_id)

    return render_template('admin/submissions.html', messages=messages,
                           unread_count=unread_count, selected=selected)


@admin.route('/submissions/<int:message_id>/read', methods=['POST'])
@login_required
def mark_read(message_id):
    msg = ContactSubmission.query.get_or_404(message_id)
    msg.is_read = True
    db.session.commit()
    return redirect(url_for('admin.submissions'))


@admin.route('/submissions/<int:message_id>/delete', methods=['POST'])
@login_required
def delete_message(message_id):
    msg = ContactSubmission.query.get_or_404(message_id)
    db.session.delete(msg)
    db.session.commit()
    flash('Message deleted.', 'success')
    return redirect(url_for('admin.submissions'))


@admin.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    form = MatricResultForm()
    if form.validate_on_submit():
        existing = MatricResult.query.filter_by(year=form.year.data).first()
        if existing:
            existing.candidates = form.candidates.data
            existing.pass_rate = form.pass_rate.data
            existing.bachelor_passes = form.bachelor_passes.data
            existing.diploma_passes = form.diploma_passes.data
            existing.higher_cert_passes = form.higher_cert_passes.data
            flash(f'{form.year.data} result updated.', 'success')
        else:
            db.session.add(MatricResult(
                year=form.year.data,
                candidates=form.candidates.data,
                pass_rate=form.pass_rate.data,
                bachelor_passes=form.bachelor_passes.data,
                diploma_passes=form.diploma_passes.data,
                higher_cert_passes=form.higher_cert_passes.data,
            ))
            flash(f'{form.year.data} result added.', 'success')
        db.session.commit()
        return redirect(url_for('admin.results'))

    all_results = MatricResult.query.order_by(MatricResult.year.desc()).all()
    return render_template('admin/results.html', form=form, results=all_results)


@admin.route('/results/<int:year>/delete', methods=['POST'])
@login_required
def delete_result(year):
    result = MatricResult.query.filter_by(year=year).first_or_404()
    db.session.delete(result)
    db.session.commit()
    flash(f'{year} result deleted.', 'success')
    return redirect(url_for('admin.results'))


@admin.route('/applications')
@login_required
def applications():
    all_apps = (ApplicationRequest.query
                .order_by(ApplicationRequest.submitted_at.desc())
                .all())
    unreviewed_count = ApplicationRequest.query.filter_by(is_reviewed=False).count()

    selected = None
    selected_id = request.args.get('selected', type=int)
    if selected_id:
        selected = ApplicationRequest.query.get_or_404(selected_id)

    return render_template('admin/applications.html', applications=all_apps,
                           unreviewed_count=unreviewed_count, selected=selected)


@admin.route('/applications/<int:app_id>/review', methods=['POST'])
@login_required
def mark_application_reviewed(app_id):
    app_req = ApplicationRequest.query.get_or_404(app_id)
    app_req.is_reviewed = True
    db.session.commit()
    return redirect(url_for('admin.applications', selected=app_id))


@admin.route('/applications/<int:app_id>/delete', methods=['POST'])
@login_required
def delete_application(app_id):
    app_req = ApplicationRequest.query.get_or_404(app_id)
    db.session.delete(app_req)
    db.session.commit()
    flash('Application request deleted.', 'success')
    return redirect(url_for('admin.applications'))
