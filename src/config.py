from os import environ


class Config:
    """Set Flask config variables."""

    FLASK_ENV = 'development'
    TESTING = True

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Elevate Endpoints Info
    ELEVATE_BASE_URL = "http://incident-api.use1stag.elevatesecurity.io"
    ELEVATE_USERNAME = environ.get('ELEVATE_USERNAME')
    ELEVATE_PASSWORD = environ.get('ELEVATE_PASSWORD')
    ELEVATE_INCIDENT_TYPES = ['other', 'denial', 'executable', 'intrusion', 'misuse', 'probing', 'unauthorized']

    # Each difference incident type has its own column as identifier, either IP or employee_id
    ELEVATE_IDENTIFIER_COL = {
        'denial': 'reported_by',
        'executable': 'machine_ip',
        'intrusion': 'internal_ip',
        'misuse': 'employee_id',
        'other': 'identifier',
        'probing': 'ip',
        'unauthorized': 'employee_id'
    }

    ELEVATE_INCIDENT_PRIORITIES = ['low', 'medium', 'high', 'critical']
