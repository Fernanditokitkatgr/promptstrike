from abc import ABC, abstractmethod
from vuln_bot.bot import fake_llm, ollama_llm, fake_llm_document
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


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


class DocumentTarget(Target):
    def __init__(self, system_prompt, document):
        self.system_prompt = system_prompt
        self.document = document

    def send(self, message):
        return fake_llm_document(self.system_prompt, message, self.document)


class APITarget(Target):
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.client = OpenAI()

    def send(self, message):
        respuesta = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message},
            ],
        )
        return respuesta.choices[0].message.content


def create_target(nombre, system_prompt):
    if nombre == "local":
        return LocalTarget(system_prompt)
    elif nombre == "ollama":
        return OllamaTarget(system_prompt)
    elif nombre == "api":
        return APITarget(system_prompt)
    else:
        raise ValueError("Target desconocido: '" + nombre +
                         "'. Valores válidos: 'local', 'ollama', 'api'")
