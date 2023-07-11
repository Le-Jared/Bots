# Import the libraries
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

# Custom logic adapter
class LowConfidenceAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):
        # Let's say we consider a confidence below 0.5 to be low confidence
        if self.get_most_frequent_response(statement).confidence < 0.5:
            response = Statement(text="I don't know")
            response.confidence = 1
        else:
            response = self.get_most_frequent_response(statement)

        return response

# Create a new chat bot named Charlie
chatbot = ChatBot(
    'Charlie',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        {'import_path': 'LowConfidenceAdapter'}
    ]
)

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english.greetings")
trainer.train("chatterbot.corpus.english.conversations")

# Get a response to an input statement
while True:
    try:
        user_input = input("User: ")
        response = chatbot.get_response(user_input)
        print("ChatBot: ", response)

    except(KeyboardInterrupt, EOFError, SystemExit):
        break
