import unittest
from flask_testing import TestCase
from flask import url_for
from datetime import datetime

from add_plant import app, db, Houseplants, Waterings

class TestBase(TestCase):

    def create_app(self):
        app.config['SQLALchemy_DATABASE_URI'] = "sqlite:///"
        SECRET_KEY='KEY'
        return app
    
    def setUp(self):
        db.drop_all()
        db.create_all()
        plant1 = Houseplants(houseplant_name='philodendron')
        db.session.add(plant1)
        db.session.commit()
        watering1 = Waterings(plant_id=1, date='2020-12-12')
        db.session.add(watering1)
        db.session.commit()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestAccess(TestBase):

    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code,200)

class TestAdd(TestBase):
    def test_add_plant(self):
        response = self.client.post(url_for('add'),data = dict(houseplant_name="Cactus")
        )
        self.assertIn(b'Cactus',response.data)

class TestUpdate(TestBase):
    def test_update_plant(self):
        response = self.client.post(url_for('update_plant', plant_id=1),
            data = dict(id=1, houseplant_name="Jungle Cactus"),
            follow_redirects=True
            )
        self.assertEqual(response.status_code,200)

class TestDelete(TestBase):
    def test_delete_post(self):
        response = self.client.post(url_for('delete_plant', plant_id=1), data = dict(id=1),
            follow_redirects=True
            )
        self.assertEqual(response.status_code,200)
        
class TestCare(TestBase):
    def test_care(self):
        response = self.client.post(url_for('care', plant_id=1),data = dict(plant_id=1, date='2019-12-01'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

class TestDeleteCare(TestBase):
    def test_delete_care(self):
        response = self.client.post(url_for('delete_care', watering_id=1), data=dict(watering_id=1), follow_redirects=True)
        self.assertEqual(response.status_code, 200)