from flask import jsonify


def success_envelope(payload):
    return jsonify({'status': 1, 'payload': payload})


def error_envelope(error_title, error_message):
    return jsonify({'status': 0, 'error_title': error_title, 'error_message': error_message})