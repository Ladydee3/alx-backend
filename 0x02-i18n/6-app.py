#!/usr/bin/env python3
"""A simple Flask app with locale selection based on priority."""

from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config(object):
    """Configuration for supported languages and default settings."""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Configure the Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

# Mock user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Returns a user dictionary or None if the ID is not found."""
    login_id = request.args.get('login_as')
    if login_id and login_id.isdigit():
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """Set the user information in the global context before each request."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """Selects the best match for the locale based on priority order."""
    # Priority 1: Locale from URL parameters
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # Priority 2: Locale from user settings
    if g.user:
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    # Priority 3: Locale from request Accept-Language header
    locale = request.accept_languages.best_match(app.config['LANGUAGES'])
    if locale:
        return locale

    # Priority 4: Default locale
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/')
def index():
    """Render the main page."""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)

