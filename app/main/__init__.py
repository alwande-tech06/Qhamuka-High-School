from flask import Blueprint, render_template, redirect, url_for, flash

from app.models import db, Announcement, Gallery, ContactSubmission
from app.forms import ContactForm

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


@main.route('/academics')
def academics():
    return render_template('main/academics.html')


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
