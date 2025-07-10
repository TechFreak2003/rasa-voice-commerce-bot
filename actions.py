from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

print("✅ actions.py loaded")


class ActionGetAllProducts(Action):
    def name(self) -> Text:
        return "action_get_all_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            response = requests.get("http://localhost:5000/api/products")
            products = response.json()
            if not products:
                dispatcher.utter_message(text="No products found.")
            else:
                product_list = "\n".join([f"- {p['name']} (₹{p['price']})" for p in products])
                dispatcher.utter_message(text=f"Here are some products:\n{product_list}")
        except:
            dispatcher.utter_message(text="Failed to fetch products. Please try again later.")

        return []

class ActionGetProductById(Action):
    def name(self) -> Text:
        return "action_get_product_by_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product_id = tracker.get_slot("product_id")

        try:
            response = requests.get(f"http://localhost:5000/api/products/{product_id}")
            if response.status_code == 404:
                dispatcher.utter_message(text="Product not found.")
            else:
                product = response.json()
                dispatcher.utter_message(
                    text=f"{product['name']}: {product['description']}\nPrice: ₹{product['price']}\nStock: {product['countInStock']}"
                )
        except:
            dispatcher.utter_message(text="Could not fetch product details.")

        return []


class ActionAddToCart(Action):
    def name(self) -> Text:
        return "action_add_to_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        item = tracker.get_slot("item")
        quantity = tracker.get_slot("quantity") or 1

        try:
            payload = {
                "productId": item,
                "quantity": int(quantity)
            }
            response = requests.post("http://localhost:5000/api/cart", json=payload)
            if response.status_code == 201:
                dispatcher.utter_message(text=f"Added {quantity} x {item} to your cart.")
            else:
                dispatcher.utter_message(text="Could not add the item to your cart.")
        except:
            dispatcher.utter_message(text="Error connecting to the cart service.")

        return []

class ActionViewCart(Action):
    def name(self) -> Text:
        return "action_view_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            response = requests.get("http://localhost:5000/api/cart")
            cart = response.json()
            if not cart or not cart.get("items"):
                dispatcher.utter_message(text="Your cart is empty.")
            else:
                items = cart["items"]
                message = "Your cart contains:\n"
                for item in items:
                    message += f"- {item['product']['name']} x {item['quantity']}\n"
                dispatcher.utter_message(text=message)
        except:
            dispatcher.utter_message(text="Could not fetch your cart.")

        return []

class ActionRemoveFromCart(Action):
    def name(self) -> Text:
        return "action_remove_from_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        item_id = tracker.get_slot("item_id")

        try:
            response = requests.delete(f"http://localhost:5000/api/cart/{item_id}")
            if response.status_code == 200:
                dispatcher.utter_message(text="Item removed from your cart.")
            else:
                dispatcher.utter_message(text="Could not remove the item from your cart.")
        except:
            dispatcher.utter_message(text="Failed to connect to the cart service.")

        return []

class ActionUpdateCartItem(Action):
    def name(self) -> Text:
        return "action_update_cart_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        item_id = tracker.get_slot("item_id")
        quantity = tracker.get_slot("quantity")

        try:
            payload = {"quantity": int(quantity)}
            response = requests.put(f"http://localhost:5000/api/cart/{item_id}", json=payload)
            if response.status_code == 200:
                dispatcher.utter_message(text=f"Updated quantity of item {item_id} to {quantity}.")
            else:
                dispatcher.utter_message(text="Could not update the cart item.")
        except:
            dispatcher.utter_message(text="Could not update your cart at this time.")

        return []

class ActionClearCart(Action):
    def name(self) -> Text:
        return "action_clear_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            response = requests.delete("http://localhost:5000/api/cart/clear")
            if response.status_code == 200:
                dispatcher.utter_message(text="Your cart has been cleared.")
            else:
                dispatcher.utter_message(text="Could not clear your cart.")
        except:
            dispatcher.utter_message(text="Failed to connect to the cart service.")

        return []


class ActionCheckout(Action):
    def name(self) -> Text:
        return "action_checkout"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            response = requests.post("http://localhost:5000/api/checkout")
            payment_link = response.json().get("payment_url", "http://example.com/payment")
            dispatcher.utter_message(text=f"Proceed to payment here: {payment_link}")
        except:
            dispatcher.utter_message(text="Checkout failed. Please try again later.")

        return []

class ActionViewMyOrders(Action):
    def name(self) -> Text:
        return "action_view_my_orders"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            response = requests.get("http://localhost:5000/api/orders")
            orders = response.json()
            if not orders:
                dispatcher.utter_message(text="You have no orders yet.")
            else:
                message = "Here are your orders:\n"
                for order in orders:
                    message += f"Order #{order['_id']}: ₹{order['totalPrice']}\n"
                dispatcher.utter_message(text=message)
        except:
            dispatcher.utter_message(text="Could not fetch your orders.")

        return []

class ActionViewAllOrders(Action):
    def name(self) -> Text:
        return "action_view_all_orders"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            response = requests.get("http://localhost:5000/api/admin/orders")
            orders = response.json()
            if not orders:
                dispatcher.utter_message(text="No orders found.")
            else:
                message = "Admin orders:\n"
                for order in orders:
                    message += f"Order #{order['_id']} by {order['user']['name']} - ₹{order['totalPrice']}\n"
                dispatcher.utter_message(text=message)
        except:
            dispatcher.utter_message(text="Could not fetch admin orders.")

        return []
