import grpc
from concurrent import futures
from hashport import hashport
import socket
from uuid import uuid5, NAMESPACE_DNS
from shopping_pb2 import Seller, Product, UpdateProductReq, DeleteProductReq, ShowProductReq, Response, PingReq
import shopping_pb2_grpc as shopping_pb2_grpc


def run(server_addr, seller_uuid, ip, port):
    try:
        # Create a gRPC channel to connect to the server
        channel = grpc.insecure_channel(server_addr)
        # Create a stub for the ShoppingApp service
        stub = shopping_pb2_grpc.ShoppingAppStub(channel)
        stub.checkConnection(PingReq(message="Connection Request from Seller"))
    except:
        print('\nServer offline\n')
        exit(1)

    print('\nConnected to server\n')

    ops = ('Register Seller', 'Sell Product', 'Update Product', 'Delete Product',
           "Show Seller's Products", 'Exit')
    ops = [f'{i+1}. {op}' for i, op in enumerate(ops)]

    while True:
        print()
        choice = input('\n'.join(ops) + '\nEnter Choice: ')

        match choice:
            case '1':
                seller = Seller(uuid=seller_uuid,
                                notif_server_addr=ip+':'+str(port))
                try:
                    response = stub.regSeller(seller)
                    print(f'Response: {response.message}')
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '2':
                details = input(
                    "Enter product details (name, category, price, quantity, description): ")
                name, category, price, qty, descr = details.split(', ')

                # PID = '-1' to indicate that the server should assign a new PID
                product = Product(pid='-1', seller_uuid=seller_uuid, name=name, price=int(
                    price), cat=category, qty=int(qty), rating=float(0), desc=descr)
                try:
                    response = stub.sellProduct(product)

                    print(f'\nResponse: {response.message}')
                    if response.status:
                        print(f"Assigned Product ID: {response.product_id}")
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '3':
                pid = input("Enter product ID: ")
                update_details = input(
                    "Enter new details (name, category, price, quantity, description): ")
                name, category, price, qty, descr = update_details.split(', ')

                update_req = UpdateProductReq(product_id=pid, seller_uuid=seller_uuid, new_product=Product(
                    pid=pid, seller_uuid=seller_uuid, name=name, price=int(price), cat=category, qty=int(qty), desc=descr))
                try:
                    response = stub.updateProduct(update_req)
                    print(f'\nResponse: {response.message}')
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '4':
                pid = input("Enter product ID: ")

                delete_req = DeleteProductReq(
                    product_id=pid, seller_uuid=seller_uuid)
                try:
                    response = stub.deleteProduct(delete_req)
                    print(f'\nResponse: {response.message}')
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '5':
                show_products_req = ShowProductReq(seller_uuid=seller_uuid)

                print(f'\nList of products:')
                try:
                    for product in stub.showProducts(show_products_req):
                        print(str(product))
                except:
                    print('\nServer offline\n')
                    exit(1)

            case '6':
                break

            case _:
                continue


class SellerNotificationServicer(shopping_pb2_grpc.SellerNotificationServicer):
    def __init__(self):
        pass

    def notifyConnection(self, request, context):
        print('\nNew notification:\n' + str(request))
        return Response(status=True, message="Notification received")

    def notifyProductBought(self, request, context):
        print('\nNew notification:')
        print('Product bought notification:\n', str(request))
        return Response(status=True, message="Notification received")


def serve(port, ip, seller_uuid, server_addr):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_SellerNotificationServicer_to_server(
        SellerNotificationServicer(), server)
    server.add_insecure_port('[::]:'+str(port))
    server.start()
    print(f'Seller notification server started on port {port}\n')
    # server.wait_for_termination()
    run(server_addr=server_addr, seller_uuid=seller_uuid, ip=ip, port=port)


def authenticate():
    server_ip = input("Enter market server's IP address: ")
    server_port = input("Enter market server's Port Number: ")
    server_addr = server_ip + ':' + server_port

    username = input("Enter username: ")
    port = hashport(username)
    print(f'Port: {port}')

    seller_uuid = uuid5(NAMESPACE_DNS, username).hex
    print(f'Seller UUID: {seller_uuid}')
    return server_addr, seller_uuid, port


if __name__ == '__main__':
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    print("Seller IP Address:", ip)

    server_addr, seller_uuid, port = authenticate()
    serve(port=port, ip=ip, seller_uuid=seller_uuid, server_addr=server_addr)
