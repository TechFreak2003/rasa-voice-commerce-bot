from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

print("✅ actions.py loaded")

class ActionAddToCart(Action):
    def name(self) -> Text:
        return "action_add_to_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        item = tracker.get_slot('item')
        # You can replace this with a real API call
        response = requests.post("http://localhost:5000/api/cart", json={"item": item})
        
        dispatcher.utter_message(text=f"{item} has been added to your cart.")
        return []

class ActionCheckout(Action):
    def name(self) -> Text:
        return "action_checkout"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Mock: Call checkout API
        response = requests.post("http://localhost:5000/api/checkout")

        payment_link = response.json().get("payment_url", "http://example.com/payment")

        dispatcher.utter_message(text=f"Proceeding to payment. Click here: {payment_link}")
        return []