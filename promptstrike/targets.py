from vuln_bot.bot import fake_llm


class LocalTarget:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt

    def send(self, message):
        return fake_llm(self.system_prompt, message)
