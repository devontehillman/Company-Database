from pytest import *
from employee_student import Salaried

@fixture
def salaried():
    return Salaried("John","John@acme-machining.com",60000)


"""
Test for salary 
Things to check.
    - raises ValueError for negative 
    - raises ValueError for under50k 
    - Can set an image
    - __repr__ works
"""
"""5 for each setter setter functions

5 constructor
name, email, id, image, yearly
"""

def test_name_is_string(salaried):
    pass

def email_has_correct_adress(salaried):
    pass



def test_salaried(salaried):
    assert salaried.yearly == 60000

def test_salaried_negative(salaried):
    with raises(ValueError):
        salaried.yearly = -1

def test_salaried_under50k(salaried):
    with raises(ValueError):
        salaried.yearly = 20000

def test_salaried_image(salaried):
    salaried.image = "main/assets/face.jpg"
    assert type(salaried.image) == str
