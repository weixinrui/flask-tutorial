import logging
from flask import has_request_context, request, session

class RequestFormatter(logging.Formatter):
    
    def format(self, record):
        if has_request_context(record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method
            record.form = dict(request.form)
            record.files = dict(request.files)
            record.json = dict(request.json)
        else:
            record.url = None
            record.remote_addr = None
            record.method = None
            record.form = None
            record.files = None
            record.json = None
        return super(RequestFormatter, self).format(record)
    

formatter = RequestFormatter(
    '[%(asctime)s] %(levelname)s %(remote_addr)s %(method)s %(url)s\n'
    '%(filename)s: %(message)s (%(lineno)d'
)