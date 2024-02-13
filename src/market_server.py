import grpc
from concurrent import futures
from shopping_pb2 import RegProductResponse, Response, ProductBoughtNotif, ProductUpdatedNotif, ProductForDisplay, PingReq
import shopping_pb2_grpc as shopping_pb2_grpc


class ShoppingAppServicer(shopping_pb2_grpc.ShoppingAppServicer):
    def __init__(self):
        self.seller_db = {}
        self.product_db = {}
        self.buyer_db = {}
        self.wishlist_db = {}
        self.rating_db = {}

    def checkConnection(self, request, context):
        print('Connection request:\n', str(request))
        print('Accepted\n')
        return Response(status=True, message="Connection successful")

    # Seller methods
    def regSeller(self, request, context):
        print('Seller registration request:\n', str(request))

        if request.uuid not in self.seller_db:
            try:
                # Create a gRPC channel to connect to the server
                channel = grpc.insecure_channel(request.notif_server_addr)
                # Create a stub for the ShoppingApp service
                stub = shopping_pb2_grpc.SellerNotificationStub(channel)
                stub.notifyConnection(PingReq(message="Connected"))
            except:
                print('\nNotification server offline\n')
                return Response(status=False, message="Notification server offline")
            
            print("Connected to seller's notification server")

            self.seller_db[request.uuid] = {
                'notif_server_addr': request.notif_server_addr, 'products': set(), 'stub': stub}

            print('Accepted\n')
            # print(self.seller_db)
            # print()

            return Response(status=True, message="Seller registered successfully")
        else:
            print('Rejected\n')
            return Response(status=False, message="Seller already registered")

    def sellProduct(self, request, context):
        print('Product sale request:\n', str(request))

        if request.seller_uuid in self.seller_db:
            pid = '0'
            if len(self.product_db):
                pid = str(int(sorted(self.product_db.keys())[-1])+1)
            self.product_db[pid] = request
            self.product_db[pid].pid = pid
            self.seller_db[request.seller_uuid]['products'].add(pid)

            print('Accepted\n')
            # print(self.seller_db)
            # print(self.product_db)
            # print()
            return RegProductResponse(status=True, message="Product registered successfully", product_id=pid)
        else:
            print('Rejected\n')
            return RegProductResponse(status=False, message="Seller not registered", product_id='-1')

    def updateProduct(self, request, context):
        print('Product update request:\n', str(request))

        if request.product_id in self.product_db:
            if request.seller_uuid == self.product_db[request.product_id].seller_uuid:
                rating = self.product_db[request.product_id].rating
                self.product_db[request.product_id] = request.new_product
                self.product_db[request.product_id].rating = rating

                # Notify buyers
                for buyer_uuid in self.wishlist_db.get(request.product_id, []):
                    stub = self.buyer_db[buyer_uuid]['stub']
                    req = ProductUpdatedNotif(new_product=ProductForDisplay(pid=request.new_product.pid,
                                                                            name=request.new_product.name,
                                                                            cat=request.new_product.cat,
                                                                            price=request.new_product.price,
                                                                            rating=rating,
                                                                            desc=request.new_product.desc))
                    stub.notifyProductUpdated(req)

                print("Accepted\n")
                # print(self.product_db)
                # print()
                return Response(status=True, message="Product updated successfully")
            else:
                print("Rejected\n")
                return Response(status=False, message="You are not authorized to perform this operation")
        else:
            print("Rejected\n")
            return Response(status=False, message="Product not found")

    def deleteProduct(self, request, context):
        print('Product delete request:\n', str(request))

        if request.product_id in self.product_db:
            if request.seller_uuid == self.product_db[request.product_id].seller_uuid:
                self.seller_db[request.seller_uuid]['products'].remove(
                    request.product_id)
                del self.product_db[request.product_id]

                if request.product_id in self.wishlist_db:
                    del self.wishlist_db[request.product_id]
                if request.product_id in self.rating_db:
                    del self.rating_db[request.product_id]

                for buyer in self.buyer_db:
                    if request.product_id in self.buyer_db[buyer]['wishlist']:
                        self.buyer_db[buyer]['wishlist'].remove(request.product_id)

                print("Accepted\n")
                # print(self.seller_db)
                # print(self.product_db)
                # print()
                return Response(status=True, message="Product deleted successfully")
            else:
                print("Rejected\n")
                return Response(status=False, message="Seller not authorized")
        else:
            print("Rejected\n")
            return Response(status=False, message="Product not found")

    def showProducts(self, request, context):
        print('Show product request:\n', str(request))

        if request.seller_uuid in self.seller_db:
            products = [self.product_db[pid]
                        for pid in self.seller_db[request.seller_uuid]['products']]

            print("Accepted\n")
            # print(products)
            # print()
            for product in products:
                yield product
        else:
            print("Rejected\n")
            return []

    # Buyer methods
    def regBuyer(self, request, context):
        print('Buyer registration request:\n', str(request))

        if request.uuid not in self.buyer_db:
            try:
                # Create a gRPC channel to connect to the server
                channel = grpc.insecure_channel(request.notif_server_addr)
                # Create a stub for the ShoppingApp service
                stub = shopping_pb2_grpc.BuyerNotificationStub(channel)
                stub.notifyConnection(PingReq(message="Connected"))
            except:
                print('\nNotification server offline\n')
                return Response(status=False, message="Notification server offline")
            
            print("Connected to buyer's notification server")

            self.buyer_db[request.uuid] = {
                'notif_server_addr': request.notif_server_addr, 'stub': stub, 'wishlist': set()}

            print('Accepted\n')
            # print(self.buyer_db)
            # print()

            return Response(status=True, message="Buyer registered successfully")
        else:
            print('Rejected\n')
            return Response(status=False, message="Buyer already registered")

    def browseProducts(self, request, context):
        print('Browse products request:\n', str(request))

        products = []
        if request.product_name:
            products = [self.product_db[pid]
                        for pid in self.product_db if request.product_name in self.product_db[pid].name]
        elif request.cat_name:
            products = [self.product_db[pid]
                        for pid in self.product_db if request.cat_name in self.product_db[pid].cat]
        else:
            products = list(self.product_db.values())

        products = [ProductForDisplay(
            pid=x.pid, name=x.name, price=x.price, cat=x.cat, rating=x.rating, desc=x.desc) for x in products if x.qty > 0]

        print("Accepted\n")
        # print(products)
        # print()
        for product in products:
            yield product

    def buyProduct(self, request, context):
        print('Buy product request:\n', str(request))

        if request.product_id in self.product_db:
            if request.qty <= self.product_db[request.product_id].qty:
                self.product_db[request.product_id].qty -= request.qty

                # Notify seller
                seller_uuid = self.product_db[request.product_id].seller_uuid
                stub = self.seller_db[seller_uuid]['stub']
                req = ProductBoughtNotif(
                    product_id=request.product_id,  qty=request.qty)

                stub.notifyProductBought(req)
                print("Accepted\n")
                # print()
                return Response(status=True, message="Product bought successfully")
            else:
                print("Rejected\n")
                return Response(status=False, message="Quantity insufficient")
        else:
            print("Rejected\n")
            return Response(status=False, message="Product not found")

    def addToWishlist(self, request, context):
        print('Add to wishlist request:\n', str(request))

        if request.product_id in self.product_db:
            if not self.wishlist_db.get(request.product_id, None):
                self.wishlist_db[request.product_id] = set()
            self.wishlist_db[request.product_id].add(request.buyer_uuid)
            self.buyer_db[request.buyer_uuid]['wishlist'].add(request.product_id)

            print("Accepted\n")
            # print()
            return Response(status=True, message="Product added to wishlist successfully")
        else:
            print("Rejected\n")
            return Response(status=False, message="Product not found")

    def viewWishlist(self, request, context):
        print('View wishlist request:\n', str(request))

        products = []
        if request.buyer_uuid in self.buyer_db:
            products = [self.product_db[pid]
                        for pid in self.buyer_db[request.buyer_uuid]['wishlist']]

        products = [ProductForDisplay(
            pid=x.pid, name=x.name, price=x.price, cat=x.cat, rating=x.rating, desc=x.desc) for x in products]

        print("Accepted\n")
        # print(products)
        # print()
        for product in products:
            yield product

    def rateProduct(self, request, context):
        print('Rate product request:\n', str(request))

        if request.product_id in self.product_db:
            if not self.rating_db.get(request.product_id, None):
                self.rating_db[request.product_id] = dict()
            self.rating_db[request.product_id][request.buyer_uuid] = request.rating

            self.product_db[request.product_id].rating = sum(list(
                self.rating_db[request.product_id].values())) / len(self.rating_db[request.product_id])

            print("Accepted\n")
            print(self.rating_db[request.product_id])
            print(self.product_db[request.product_id].rating)
            print()
            return Response(status=True, message="Product rated successfully")
        else:
            print("Rejected\n")
            return Response(status=False, message="Product not found")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_ShoppingAppServicer_to_server(
        ShoppingAppServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
