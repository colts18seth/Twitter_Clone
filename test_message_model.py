import os
from unittest import TestCase
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class MessageModelTestCase(TestCase):
    """Test  messages Model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_repr_method(self):
        """Does repr method work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=1
        )

        db.session.add(u)
        db.session.commit()

        m = Message(
            text="New Message!",
            user_id=1
        )

        db.session.add(m)
        db.session.commit()

        msg = Message.query.one()
        self.assertIn("New Message!", repr(msg))

    def test_add_message(self):
        """Can message be added"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            id=1
        )

        db.session.add(u)
        db.session.commit()

        m = Message(
            text="New Message!",
            user_id=1
        )

        db.session.add(m)
        db.session.commit()        

        self.assertTrue(Message.query.one())
        self.assertTrue(u.messages)