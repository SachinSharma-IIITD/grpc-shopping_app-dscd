import grpc
from concurrent import futures
from shopping_pb2 import Response
import shopping_pb2_grpc as shopping_pb2_grpc


class SellerNotificationServicer(shopping_pb2_grpc.SellerNotificationServicer):
    def __init__(self):
        pass

    def notifyConnection(self, request, context):
        print(str(request))
        return Response(status=True, message="Notification received")
    
    def notifyProductBought(self, request, context):
        print('Product bought notification: \n', str(request))
        return Response(status=True, message="Notification received")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_SellerNotificationServicer_to_server(
        SellerNotificationServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
