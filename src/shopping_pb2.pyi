from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Product(_message.Message):
    __slots__ = ("seller_uuid", "pid", "name", "cat", "price", "qty", "rating", "desc")
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QTY_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    seller_uuid: str
    pid: str
    name: str
    cat: str
    price: int
    qty: int
    rating: float
    desc: str
    def __init__(self, seller_uuid: _Optional[str] = ..., pid: _Optional[str] = ..., name: _Optional[str] = ..., cat: _Optional[str] = ..., price: _Optional[int] = ..., qty: _Optional[int] = ..., rating: _Optional[float] = ..., desc: _Optional[str] = ...) -> None: ...

class ProductForDisplay(_message.Message):
    __slots__ = ("pid", "name", "cat", "price", "rating", "desc")
    PID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    pid: str
    name: str
    cat: str
    price: int
    rating: float
    desc: str
    def __init__(self, pid: _Optional[str] = ..., name: _Optional[str] = ..., cat: _Optional[str] = ..., price: _Optional[int] = ..., rating: _Optional[float] = ..., desc: _Optional[str] = ...) -> None: ...

class Seller(_message.Message):
    __slots__ = ("uuid", "notif_server_addr")
    UUID_FIELD_NUMBER: _ClassVar[int]
    NOTIF_SERVER_ADDR_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    notif_server_addr: str
    def __init__(self, uuid: _Optional[str] = ..., notif_server_addr: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: bool
    message: str
    def __init__(self, status: bool = ..., message: _Optional[str] = ...) -> None: ...

class RegProductResponse(_message.Message):
    __slots__ = ("status", "message", "product_id")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    status: bool
    message: str
    product_id: str
    def __init__(self, status: bool = ..., message: _Optional[str] = ..., product_id: _Optional[str] = ...) -> None: ...

class UpdateProductReq(_message.Message):
    __slots__ = ("seller_uuid", "product_id", "new_product")
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_PRODUCT_FIELD_NUMBER: _ClassVar[int]
    seller_uuid: str
    product_id: str
    new_product: Product
    def __init__(self, seller_uuid: _Optional[str] = ..., product_id: _Optional[str] = ..., new_product: _Optional[_Union[Product, _Mapping]] = ...) -> None: ...

class DeleteProductReq(_message.Message):
    __slots__ = ("seller_uuid", "product_id")
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    seller_uuid: str
    product_id: str
    def __init__(self, seller_uuid: _Optional[str] = ..., product_id: _Optional[str] = ...) -> None: ...

class ShowProductReq(_message.Message):
    __slots__ = ("seller_uuid",)
    SELLER_UUID_FIELD_NUMBER: _ClassVar[int]
    seller_uuid: str
    def __init__(self, seller_uuid: _Optional[str] = ...) -> None: ...

class BrowseProductsReq(_message.Message):
    __slots__ = ("buyer_uuid", "product_name", "cat_name")
    BUYER_UUID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    CAT_NAME_FIELD_NUMBER: _ClassVar[int]
    buyer_uuid: str
    product_name: str
    cat_name: str
    def __init__(self, buyer_uuid: _Optional[str] = ..., product_name: _Optional[str] = ..., cat_name: _Optional[str] = ...) -> None: ...

class BuyProductReq(_message.Message):
    __slots__ = ("buyer_uuid", "product_id", "qty")
    BUYER_UUID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    QTY_FIELD_NUMBER: _ClassVar[int]
    buyer_uuid: str
    product_id: str
    qty: int
    def __init__(self, buyer_uuid: _Optional[str] = ..., product_id: _Optional[str] = ..., qty: _Optional[int] = ...) -> None: ...

class WishlistReq(_message.Message):
    __slots__ = ("buyer_uuid", "product_id")
    BUYER_UUID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    buyer_uuid: str
    product_id: str
    def __init__(self, buyer_uuid: _Optional[str] = ..., product_id: _Optional[str] = ...) -> None: ...

class ViewWishlistReq(_message.Message):
    __slots__ = ("buyer_uuid",)
    BUYER_UUID_FIELD_NUMBER: _ClassVar[int]
    buyer_uuid: str
    def __init__(self, buyer_uuid: _Optional[str] = ...) -> None: ...

class RateProductReq(_message.Message):
    __slots__ = ("buyer_uuid", "product_id", "rating")
    BUYER_UUID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    buyer_uuid: str
    product_id: str
    rating: float
    def __init__(self, buyer_uuid: _Optional[str] = ..., product_id: _Optional[str] = ..., rating: _Optional[float] = ...) -> None: ...

class Buyer(_message.Message):
    __slots__ = ("uuid", "notif_server_addr")
    UUID_FIELD_NUMBER: _ClassVar[int]
    NOTIF_SERVER_ADDR_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    notif_server_addr: str
    def __init__(self, uuid: _Optional[str] = ..., notif_server_addr: _Optional[str] = ...) -> None: ...

class ProductBoughtNotif(_message.Message):
    __slots__ = ("product_id", "qty")
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    QTY_FIELD_NUMBER: _ClassVar[int]
    product_id: str
    qty: int
    def __init__(self, product_id: _Optional[str] = ..., qty: _Optional[int] = ...) -> None: ...

class ProductUpdatedNotif(_message.Message):
    __slots__ = ("new_product",)
    NEW_PRODUCT_FIELD_NUMBER: _ClassVar[int]
    new_product: ProductForDisplay
    def __init__(self, new_product: _Optional[_Union[ProductForDisplay, _Mapping]] = ...) -> None: ...

class PingReq(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
