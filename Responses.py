from datetime import datetime

def sample_responses(input_text, datetime=None):
    user_messages = str(input_text).lower()


    if user_messages not in ("hello", "hi",):
        if user_messages in ("who are you?", "who are you"):
         return "I am PytutBot"

        if user_messages in ("i'm Cool", "cool", "am cool","nothing much", "nothing really", "Same old, same old"):
            return "That's great!!!"


        if user_messages in ("time", "time?"):
            now = datetime.now()
            datetime = now.strftime("%d/%m/%y, %H:%M:%S")

            return str(datetime)
        return "I dont understand you please."

    return "Hey what's up?"



