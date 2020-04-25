import json
import falcon

class JSONTranslator(object):
    def process_request(self, req, res):
        if req.content_type == 'application/json':
            try:
                raw_json = req.stream.read()
            except Exception:
                message = 'Read Error'
                raise falcon('Bad request', message)
            if raw_json:
                req.context['data'] = json.loads(raw_json.decode('utf-8'))
        else:
            req.context['data'] = None