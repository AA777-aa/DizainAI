"""
Клиент для работы с OpenAI GPT API
"""

import json
from typing import Optional, Dict, List, Callable
from dataclasses import dataclass
import openai
from openai import OpenAI


@dataclass
class GPTResponse:
    """Ответ от GPT"""
    success: bool
    content: str = ""
    error: str = ""
    tokens_used: int = 0


class GPTClient:
    """Клиент для GPT API"""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.api_key = api_key
        self.model = model
        self.client: Optional[OpenAI] = None
        self._init_client()

    def _init_client(self):
        """Инициализация клиента OpenAI"""
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)

    def set_api_key(self, api_key: str):
        """Установить API ключ"""
        self.api_key = api_key
        self._init_client()

    def is_configured(self) -> bool:
        """Проверка настройки API"""
        return bool(self.api_key and self.client)

    def send_message(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> GPTResponse:
        """
        Отправить сообщение в GPT

        Args:
            messages: Список сообщений [{"role": "user/system/assistant", "content": "..."}]
            temperature: Креативность (0-1)
            max_tokens: Максимум токенов в ответе

        Returns:
            GPTResponse с результатом
        """
        if not self.is_configured():
            return GPTResponse(
                success=False,
                error="API ключ не настроен. Укажите ключ в настройках."
            )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            content = response.choices[0].message.content
            tokens = response.usage.total_tokens if response.usage else 0

            return GPTResponse(
                success=True,
                content=content,
                tokens_used=tokens
            )

        except openai.AuthenticationError:
            return GPTResponse(
                success=False,
                error="Неверный API ключ. Проверьте настройки."
            )
        except openai.RateLimitError:
            return GPTResponse(
                success=False,
                error="Превышен лимит запросов. Подождите немного."
            )
        except openai.APIConnectionError:
            return GPTResponse(
                success=False,
                error="Ошибка подключения. Проверьте интернет."
            )
        except Exception as e:
            return GPTResponse(
                success=False,
                error=f"Ошибка: {str(e)}"
            )

    def send_simple(self, prompt: str, system_prompt: str = "") -> GPTResponse:
        """Упрощённая отправка одного запроса"""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        return self.send_message(messages)