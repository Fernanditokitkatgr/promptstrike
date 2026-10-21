from abc import ABC, abstractmethod
from vuln_bot.bot import fake_llm, ollama_llm


class Target(ABC):
    @abstractmethod
    def send(self, message):
        pass


class LocalTarget(Target):
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt

    def send(self, message):
        return fake_llm(self.system_prompt, message)


class OllamaTarget(Target):
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt

    def send(self, message):
        return ollama_llm(self.system_prompt, message)
