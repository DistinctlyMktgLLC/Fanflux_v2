# Pages/__init__.py
print("Initializing Pages module")

from .home import app as home_app
print("Imported home_app")
from .mlb_aapi import app as mlb_aapi_app
print("Imported mlb_aapi_app")
from .mlb_americanindian import app as mlb_americanindian_app
print("Imported mlb_americanindian_app")
from .mlb_asian import app as mlb_asian_app
print("Imported mlb_asian_app")
from .mlb_black import app as mlb_black_app
print("Imported mlb_black_app")
from .mlb_hispanic import app as mlb_hispanic_app
print("Imported mlb_hispanic_app")
from .mlb_white import app as mlb_white_app
print("Imported mlb_white_app")
from .chatbot import app as chatbot_page_app
print("Imported chatbot_page_app")
