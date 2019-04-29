import unittest
from app.models import Pitch,User
from flask_login import current_user
from app import db

class TestPitch(unittest.TestCase):

   def setUp(self):
       self.user_Manka = User(username = 'Manka',
                                password = 'jhkk',
                                email = 'manka@ms.com')

       self.new_pitch = Pitch(id=12345,title='Pitch itself')

   def tearDown(self):
       Pitch.query.delete()
       User.query.delete()

   def test_instance(self):
       self.assertTrue(isinstance(self.new_pitch,Pitch))


   def test_check_instance_variables(self):
       self.assertEquals(self.new_pitch.id,12345)
       self.assertEquals(self.new_pitch.title,'Pitch itself')

   def test_save_pitch(self):
       self.new_pitch.save_pitch()
       self.assertTrue(len(Pitch.query.all())>0)


   def test_get_pitch_by_id(self):

       self.new_pitch.save_pitch()
       got_pitches = Pitch.get_pitch(12345)
       self.assertTrue(len(got_pitches) == 1)