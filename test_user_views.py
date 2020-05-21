import os
from unittest import TestCase
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class UserViewsTestCase(TestCase):
    """Test  User Views."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        self.testuser_id = 400
        self.testuser.id = self.testuser_id

        self.u1 = User.signup("abc", "test1@test.com", "password", None)
        self.u1_id = 401
        self.u1.id = self.u1_id
        self.u2 = User.signup("efg", "test2@test.com", "password", None)
        self.u2_id = 402
        self.u2.id = self.u2_id
        self.u3 = User.signup("hij", "test3@test.com", "password", None)
        self.u4 = User.signup("testing", "test4@test.com", "password", None)

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_users_list(self):
        with self.client as c:
            res = c.get("/users")

        self.assertEqual(res.status_code, 200)
        self.assertIn("@testuser", str(res.data))
        self.assertIn("@abc", str(res.data))

    def test_users_show(self):
        with self.client as c:
            res = c.get(f"/users/{self.testuser.id}")

        self.assertEqual(res.status_code, 200)
        self.assertIn("@testuser", str(res.data))

    def test_following(self):

        f = Follows(user_being_followed_id=self.u1_id, user_following_id=self.testuser_id)
        db.session.add(f)
        db.session.commit()

        with self.client as c:
            res = c.get(f"/users/{self.u1.id}/following", follow_redirects=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(Follows.query.all())

    def test_followers(self):

        f = Follows(user_being_followed_id=self.u1_id, user_following_id=self.testuser_id)
        db.session.add(f)
        db.session.commit()            

        with self.client as c:
            res = c.get(f"/users/{self.u1.id}/followers", follow_redirects=True)
        
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(Follows.query.all())
        