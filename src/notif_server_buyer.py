import grpc
from concurrent import futures
from shopping_pb2 import Response
import shopping_pb2_grpc as shopping_pb2_grpc


class BuyerNotificationServicer(shopping_pb2_grpc.BuyerNotificationServicer):
    def __init__(self):
        pass

    def notifyConnection(self, request, context):
        print(str(request))
        return Response(status=True, message="Notification received")

    def notifyProductUpdated(self, request, context):
        print('Product updated notification: \n', str(request))
        return Response(status=True, message="Notification received")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_BuyerNotificationServicer_to_server(
        BuyerNotificationServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
