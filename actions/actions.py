from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ValidateCountryForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_country_form"

    @staticmethod
    def country_db() -> List[Text]:
        #Here we want to return all the county names of the API
        
        return []

    def validate_country(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate country value."""

        if slot_value.lower() in self.country_db():
            # validation succeeded, set the value of the "country" slot to value
            return {"country": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"country": None}

class AskForSlotAction(Action):
    #custom ask for slot
    def name(self) -> Text:
        return "action_ask_country"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(text="Which country do you want to visit?")
        return []