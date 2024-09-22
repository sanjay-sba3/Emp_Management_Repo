from rest_framework.response import Response


class GetResponse(Response):
    def __init__(self, status, type, message, data):
        if not isinstance(data, list):
            data = [data]

        # Build the response structure
        response_data = {
            "status": status,
            "type": type,
            "message": message,
            "data": data if data is not None else []
        }

        # Call the parent constructor to initialize the Response object
        super().__init__(response_data, status=status)    
    
    # def __str__(self) -> str:
    #     return Response({"status":self.status,
    #                      "type":self.type,
    #                      "message":self.message,
    #                      "data":self.data},
    #                      self.status) 
    