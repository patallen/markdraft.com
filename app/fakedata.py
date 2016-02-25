from faker import Factory as FakerFactory
import factory

from models import Document, Share, User, db
from marklib.helpers import random_int


fake = FakerFactory.create()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda x: fake.user_name())
    password = "testpass"
    email = factory.LazyAttribute(lambda x: fake.email())
    first_name = factory.LazyAttribute(lambda x: fake.first_name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())


class DocumentFactory(factory.Factory):
    class Meta:
        model = Document

    title = factory.LazyAttribute(
        lambda x: fake.sentence(nb_words=3, variable_nb_words=True)
    )


def fake_users():
    for _ in xrange(1000):
        try:
            user = UserFactory()
            if user.id:
                print "IDIDIDIDIDID", user.id
            user.save()
        except Exception as e:
            print e
            pass


def fake_documents(verbose=False):
    users = User.query.all()
    for count, user in enumerate(users, 1):
        for doc in range(random_int(high=50)):
            try:
                user.documents.append(DocumentFactory())
            except Exception as e:
                print e

        if verbose:
            print "Documents for users %s/%s" % (count, len(users))

    db.session.commit()


def fake_shares(verbose=False):
    users = User.query.all()
    docs = Document.query.all()
    length = len(docs)
    for count, user in enumerate(users, 1):
        for _ in range(random_int(high=10)):
            doc = docs[random_int(high=length-1)]
            if doc not in user.documents.all():
                Share.create_or_update(user, doc, True, True, commit=False)
        if verbose:
            print "Shares for users %s/%s" % (count, len(users))
    db.session.commit()
