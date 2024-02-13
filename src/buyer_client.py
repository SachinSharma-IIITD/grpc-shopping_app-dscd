import grpc
from concurrent import futures
from hashport import hashport
import socket
from uuid import uuid5, NAMESPACE_DNS
from shopping_pb2 import Buyer, WishlistReq, BrowseProductsReq, BuyProductReq, RateProductReq, Response, ViewWishlistReq, PingReq
import shopping_pb2_grpc as shopping_pb2_grpc


def run(server_addr, buyer_uuid, ip, port):
    try:
        # Create a gRPC channel to connect to the server
        channel = grpc.insecure_channel(server_addr)
        # Create a stub for the ShoppingApp service
        stub = shopping_pb2_grpc.ShoppingAppStub(channel)
        stub.checkConnection(PingReq(message="Connection Request from Buyer"))
    except:
        print('\nServer offline\n')
        exit(1)
    
    print('\nConnected to server\n')

    ops = ('Register Buyer', 'Browse Products', 'Buy Product', 'Add Product To Wishlist', 'View My Wishlist',
           "Rate Product", 'Exit')
    ops = [f'{i+1}. {op}' for i, op in enumerate(ops)]

    while True:
        print()
        choice = input('\n'.join(ops) + '\nEnter Choice: ')

        match choice:
            case '1':
                buyer = Buyer(uuid=buyer_uuid,
                              notif_server_addr=ip+':'+str(port))
                try:
                    response = stub.regBuyer(buyer)
                    print(f'Response: {response.message}')
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '2':
                product_name = input("Enter product name: ")
                cat_name = input("Enter category name: ")
                req = BrowseProductsReq(
                    buyer_uuid=buyer_uuid, product_name=product_name, cat_name=cat_name)

                try:
                    print(f'\nList of products:')
                    for product in stub.browseProducts(req):
                        print(str(product))
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '3':
                pid = input("Enter product ID: ")
                qty = int(input("Enter Quantity: "))
                req = BuyProductReq(
                    product_id=pid, buyer_uuid=buyer_uuid, qty=qty)

                try:
                    response = stub.buyProduct(req)
                    print(f'\nResponse: {response.message}')
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '4':
                pid = input("Enter product ID: ")
                req = WishlistReq(product_id=pid, buyer_uuid=buyer_uuid)

                try:
                    response = stub.addToWishlist(req)
                    print(f'\nResponse: {response.message}')
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '5':
                req = ViewWishlistReq(buyer_uuid=buyer_uuid)

                try:
                    print(f'\nWishlist:')
                    for product in stub.viewWishlist(req):
                        print(str(product))
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '6':
                pid = input("Enter product ID: ")
                rating = float(input("Enter rating: "))
                req = RateProductReq(
                    product_id=pid, buyer_uuid=buyer_uuid, rating=rating)

                try:
                    response = stub.rateProduct(req)
                    print(f'\nResponse: {response.message}')
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '7':
                break

            case _:
                continue


class BuyerNotificationServicer(shopping_pb2_grpc.BuyerNotificationServicer):
    def __init__(self):
        pass

    def notifyConnection(self, request, context):
        print('\nNew notification:\n' + str(request))
        return Response(status=True, message="Notification received")

    def notifyProductUpdated(self, request, context):
        print('\nNew notification:')
        print('Product updated notification:\n', str(request))
        return Response(status=True, message="Notification received")


def serve(port, ip, buyer_uuid, server_addr):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_BuyerNotificationServicer_to_server(
        BuyerNotificationServicer(), server)
    server.add_insecure_port('[::]:'+str(port))
    server.start()
    print(f'Buyer Notification Server started on port {port}\n')
    # server.wait_for_termination()
    run(server_addr=server_addr, buyer_uuid=buyer_uuid, ip=ip, port=port)


def authenticate():
    server_ip = input("Enter market server's IP address: ")
    server_port = input("Enter market server's Port Number: ")
    server_addr = server_ip + ':' + server_port

    username = input("Enter username: ")
    port = hashport(username)
    print(f'Port: {port}')

    buyer_uuid = uuid5(NAMESPACE_DNS, username).hex
    print(f'Buyer UUID: {buyer_uuid}')
    return server_addr, buyer_uuid, port


if __name__ == '__main__':
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print("Buyer IP Address:", ip)

    server_addr, buyer_uuid, port = authenticate()
    serve(port=port, ip=ip, buyer_uuid=buyer_uuid, server_addr=server_addr)
