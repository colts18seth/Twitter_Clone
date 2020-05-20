import os

from unittest import TestCase

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test user Model."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)


    def test_user_repr(self):
        """Does repr method work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        usr = User.query.one()
        self.assertIn("testuser, test@test.com", repr(usr))


    def test_following(self):
        """Does is_following & is_followed_by work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        u3 = User(
            email="test3@test.com",
            username="testuser3",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        u.following.append(u2)

        self.assertTrue(u.is_following(u2))
        self.assertFalse(u.is_following(u3))
        self.assertTrue(u2.is_followed_by(u))
        self.assertFalse(u2.is_followed_by(u3))

    def test_signup(self):
        """Does signup work?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="https://homepages.cae.wisc.edu/~ece533/images/cat.png"
        )

        self.assertTrue(u)

    def test_authenticate(self):
        """Does authenticate work?"""

        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url="https://homepages.cae.wisc.edu/~ece533/images/cat.png"
        )

        auth = u.authenticate("testuser", "HASHED_PASSWORD")

        self.assertTrue(auth)