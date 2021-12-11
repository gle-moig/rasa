from typing import Text, List, Any, Dict

import requests
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

API = "https://restcountries.com/v3.1"


class ValidateCountryForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_country_form"

    def validate_country(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print(slot_value)
        response = requests.get(f"{API}/name/{slot_value.lower()}")
        if response.status_code == 200:
            print(response.json())
            if len(response.json()) == 1:
                return {"country": response.json()[0]["name"]["common"]}
            else:
                dispatcher.utter_message(f"Please be more precise, i got multiple results for {slot_value}")
        return {"country": None}

    def validate_informations(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        intent = tracker.get_intent_of_latest_message()
        country = tracker.get_slot("country")
        response = requests.get(f"{API}/name/{country}")
        if intent == "everything":
            return {"informations": response.json()[0]}
        if slot_value.lower() in response.json()[0]:
            return {"informations": response.json()[0][slot_value.lower()]}
        return {"informations": None}
