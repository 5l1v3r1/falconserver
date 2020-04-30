class SocketManager:
    def __init__(self, sio):
        self.sio = sio

    async def process_resource(self, req, resp, resource, params):
        if req.method == 'OPTIONS':
            return
        req.context['sio'] = self.sio
        
    # async def process_response(self, req, resp, resource, req_succeeded):
    #     if req.method == 'OPTIONS':
    #         return
    #     if req.context.get('socket'):
    #         if not req_succeeded:
    #             req.context['socket'].rollback()
    #         req.context['socket'].close()