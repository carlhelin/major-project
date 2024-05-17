import ollama

class LLama3:
    def __init__(self):
        self.chatbot_role = ""
        self.entity_task = ""
        self.messages = [
            {"role": "system", "content": self.chatbot_role},
            {"role": "user", "content": self.entity_task}
        ]
        self.response = None
        self.response_content = None

    def chat(self):
        if self.entity_task:
            self.response = ollama.chat(model='llama3', messages=self.messages)
            self.response_content = self.response['message']['content']
        return self.response_content

    def set_entity_task(self, entity_task):
        self.entity_task = entity_task
        self.messages = [
            {"role": "system", "content": self.chatbot_role},
            {"role": "user", "content": self.entity_task}
        ]

    def set_chatbot_role(self, chatbot_role):
        self.chatbot_role = chatbot_role
        self.messages = [
            {"role": "system", "content": self.chatbot_role},
            {"role": "user", "content": self.entity_task}
        ]

    def set_messages(self, chatbot_role, entity_task):
        self.chatbot_role = chatbot_role
        self.entity_task = entity_task
        self.messages = [
            {"role": "system", "content": self.chatbot_role},
            {"role": "user", "content": self.entity_task}
        ]

    def get_response(self):
        return self.response_content
    
    def get_messages(self):
        return self.messages

    def get_chatbot_role(self):
        return self.chatbot_role

    def get_entity_task(self):
        return self.entity_task


def main():
    llama3 = LLama3()
    llama3.set_chatbot_role("Answer just with 'Yes' or 'No'")
    llama3.set_entity_task(f"Are you good today?")
    response = llama3.chat()
    print(response)
    print("______________________")
    
if __name__ == "__main__":
    main()
    