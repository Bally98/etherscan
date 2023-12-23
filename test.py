from main import *

history = ConversationHistoryStorage()
detector = StatelessDetector(history)

user = 'User7'
message = 'tell me about aix?'
result = detector.evaluate_message(user, message)
# print(ConversationHistoryStorage.get_all_info())
print(result)

