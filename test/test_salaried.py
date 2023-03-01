from pytest import *
import sys 
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
"""5 for each setter function

5 for constructor
name, email, id, image, yearly
"""
###############name###############

def test_name_setter(salaried):
        assert salaried.name == "John"
        salaried.name = "Lucy"
        assert salaried.name == "Lucy"

def test_name_is_not_int(salaried):
    with raises(ValueError):
        salaried.name = 123

def test_name_is_not_empty(salaried):
    with raises(ValueError):
        salaried.name = ""

def test_name_is_not_space(salaried):
    with raises(ValueError):
        salaried.name = " "

def test_name_is_not_float(salaried):
    with raises(ValueError):
        salaried.name = 123.32


###############email###############
def test_email_setter(salaried):
        assert salaried.email == "John@acme-machining.com"
        salaried.name = "Lucy@acme-machining.com"
        assert salaried.name == "Lucy@acme-machining.com"

def test_email_has_correct_address(salaried):
    with raises(ValueError):
        salaried.email = "@gmail.com"

def test_email_not_space(salaried):
    with raises(ValueError):
        salaried.email = " "

def test_email_not_blank(salaried):
    with raises(ValueError):
        salaried.email = ""

def test_email_correct_address(salaried):
        assert salaried.email == "John@acme-machining.com"

###############id###############
def test_unique_id(salaried):
    employee1 = Salaried("John","John@acme-machining.com",60000)
    employee2 = Salaried("John","John@acme-machining.com",60000)
    assert employee2._id_number != employee1._id_number


###############image###############
def test_salaried_image_works(salaried):
    salaried.image = "main/assets/face.jpg"
    assert salaried.image == "main/assets/face.jpg"

def test_salaried_image_is_string(salaried):
    salaried.image = "main/assets/face.jpg"
    assert type(salaried.image) == str

def test_image_not_int(salaried):
    with raises(ValueError):
        salaried.image = 23

def test_image_not_blank(salaried):
    with raises(ValueError):
        salaried.image = ""

def test_image_not_space(salaried):
    with raises(ValueError):
        salaried.image = " "

######Salaried Yearly###########
def test_salaried_setter_for_yearly(salaried):
    assert salaried.yearly == 60000

def test_salaried_negative(salaried):
    with raises(ValueError):
        salaried.yearly = -1

def test_salaried_under50k(salaried):
    with raises(ValueError):
        salaried.yearly = 20000

def test_salaried_string(salaried):
    with raises(ValueError):
        salaried.yearly = "20000"

########Calc_pay###############
def test_calc_pay_works(salaried):
    assert salaried.calc_pay

def test_calc_pay_not_str(salaried):
    assert type(salaried.calc_pay) != str
    
def test_calc_pay_cannot_set(salaried):
    with raises(AttributeError):
        salaried.calc_pay = 10000
    
def test_calc_pay_is_float(salaried):
    assert isinstance(salaried.calc_pay, float)

def test_calc_pay_is_for_weekly(salaried):
    assert salaried.calc_pay == (salaried.yearly / 52)