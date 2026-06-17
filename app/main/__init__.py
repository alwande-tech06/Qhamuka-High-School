from flask import Blueprint, render_template, redirect, url_for, flash

from app.models import db, Announcement, Gallery, ContactSubmission, MatricResult, ApplicationRequest
from app.forms import ContactForm, ApplicationRequestForm

main = Blueprint('main', __name__)


@main.route('/')
def home():
    # Latest published announcements for the notice board
    announcements = (Announcement.query
                     .filter_by(is_published=True)
                     .order_by(Announcement.date_posted.desc())
                     .limit(3)
                     .all())
    return render_template('main/home.html', announcements=announcements)


@main.route('/announcements')
def announcements():
    posts = (Announcement.query
             .filter_by(is_published=True)
             .order_by(Announcement.date_posted.desc())
             .all())
    return render_template('main/announcements.html', announcements=posts)


@main.route('/about')
def about():
    stats = {'learners': 589, 'educators': 21, 'grades': 5}
    return render_template('main/about.html', stats=stats)


@main.route('/admissions')
def admissions():
    return render_template('main/admissions.html')


@main.route('/admissions/apply', methods=['GET', 'POST'])
def apply():
    form = ApplicationRequestForm()
    if form.validate_on_submit():
        db.session.add(ApplicationRequest(
            parent_name=form.parent_name.data,
            parent_email=form.parent_email.data,
            parent_phone=form.parent_phone.data,
            learner_first_name=form.learner_first_name.data,
            learner_last_name=form.learner_last_name.data,
            current_grade=form.current_grade.data,
            grade_applying=form.grade_applying.data,
            popia_consent=form.popia_consent.data,
        ))
        db.session.commit()
        flash('Your application request has been received. The school office will be in touch.', 'success')
        return redirect(url_for('main.admissions'))
    return render_template('main/apply.html', form=form)


@main.route('/academics')
def academics():
    results = MatricResult.query.order_by(MatricResult.year.desc()).all()
    latest = results[0] if results else None
    return render_template('main/academics.html', results=results, latest=latest)


@main.route('/gallery')
def gallery():
    photos = Gallery.query.order_by(Gallery.date_uploaded.desc()).all()
    return render_template('main/gallery.html', photos=photos)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        submission = ContactSubmission(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data,
        )
        db.session.add(submission)
        db.session.commit()
        flash('Thank you. Your message has been sent to the school office.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html', form=form)
