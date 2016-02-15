from models.users import User
from faker import Factory
from models.drafts import Document, Share
from marklib.helpers import random_int
from models import db


fake = Factory.create()


def fake_users():
    for user in xrange(1000):
        try:
            user = User({
                "username": fake.user_name(),
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            })
            user.save()
        except:
            pass


def fake_documents(verbose=False):
    users = User.query.all()
    for count, user in enumerate(users):
        for doc in range(random_int(high=50)):
            user.documents.append(
                Document({
                    "title": fake.sentence(nb_words=3, variable_nb_words=True)
                }))
        user.save()

        if verbose:
            print "Documents for users %s/%s" % (count, len(users))


def fake_shares(verbose=False):
    users = User.query.all()
    docs = Document.query.all()
    length = len(docs)
    for count, user in enumerate(users):
        for _ in range(random_int(high=10)):
            doc = docs[random_int(high=length-1)]
            if doc not in user.documents.all():
                Share.create_or_update(user, doc, True, True, commit=False)
        if verbose:
            print "Shares for users %s/%s" % (count, len(users))
    db.session.commit()
