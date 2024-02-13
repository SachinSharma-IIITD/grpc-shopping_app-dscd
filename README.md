# Shopping App using gRPC
A distributed application that simulates an online marketplace. It uses gRPC for communication between the server and client applications.

## Dependencies
1. grpc
2. grpcio-tools
4. hashport
5. protobuf

Install by running: `pip install grpcio grpcio-tools hashport protobuf`

## How to Run
1. `python market_server.py`
2. `python seller_client.py`
    [*Follow instructions in seller section*](#seller-client-side-application)
3. `python buyer_client.py`
    [*Follow instructions in buyer section*](#buyer-client-side-application)


## Market Server
Server-side implementation for a shopping application using gRPC. It handles requests from both seller and buyer clients.

> ℹ️ Market is hosted on **port 50051**


## Seller Client Side Application
Client-side implementation for a seller-side shopping application using gRPC. It allows a seller to interact with the market server through a command-line interface.

### How to Run
`python seller_client.py`

The application will prompt for  the following information:
- **Server IP Address**: *Enter server's IP address*
- **Server Port Number**: *Enter **50051***
- **Seller username**: *Enter a unique username for the seller. This will be used for creating **UUID** and **port number*** 

### 🚧 Note
> When prompted to enter product details, strictly adhere to the format:
*"product_name, category, ..."*   
The values should be ", " (comma AND space) separated, else errors will be raised.  

<div style="font-weight:300">

### User Functions
1. **Start the Application**: The user is prompted to enter the market server's IP address and port number, and a username. A unique UUID and a port number are generated for this username. This starts the gRPC notification server.
2. **Register Seller**: The application sends a regSeller request to the server with the seller's UUID and the address of the notification server.

3. **Sell Product**: The user is prompted to enter the product details. The application sends a sellProduct request to the server.

4. **Update Product**: The user is prompted to enter the product ID and the new details. The application sends an updateProduct request to the server.

5. **Delete Product**: The application sends a deleteProduct request to the server.

1. **Show Seller's Products**: The application sends a showProducts request to the server and prints the list of products of that seller.

5. **Receive Notifications**: At any time, the user may receive notifications from the server which is printed to the console.
</div>


## Buyer Client Side Application
Client-side implementation for a buyer-side shopping application using gRPC. It allows a buyer to interact with the market server through a command-line interface.

### How to run
`python buyer_client.py`
The application will prompt for  the following information:
- **Server IP Address**: *Enter apt address*
- **Server Port Number**: *Enter **50051***
- **Buyer username**: *Enter a unique username for the buyer. This will be used for creating **UUID** and **port number***

<div style="font-weight:300">

### User Functions
1. **Start the Application**: The user is prompted to enter the market server's IP address and port number, and a username. A unique UUID and a port number are generated for this username. This starts the gRPC notification server.

2. **Register Buyer**: The application sends a regBuyer request to the server with the buyer's UUID and the address of the notification server.

3. **Browse Products**: The user is prompted to enter a product name and category name. If left blank, all products are displayed.

4. **Buy Product**: The user is prompted to enter a product ID and quantity to buy.

5. **Add Product To Wishlist**: The user adds a product to wishlist.
   
6. **View Wishlist**: View products in wishlist.

7. **Rate Product**: The user gives rating to product from 1 to 5.

8. **Receive Notifications**: At any time, the user may receive notifications from the server which is printed to the console.
</div>