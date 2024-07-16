from sanic import Blueprint
from .sports import bp as sport_bp
from .events import events_bp

api = Blueprint.group(sport_bp, events_bp, url_prefix="/api")
