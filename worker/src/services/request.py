from functools import lru_cache
from typing import Optional, Any
import aiohttp
import logging

from schemas.models import UserSettings
from core.config import settings

logger = logging.getLogger("__name__")


class RequestService:
	USER_DATA_URL = settings.user_data_url
	FILM_DATA_URL = settings.film_data_url

	def __init__(self):
		...

	async def make_request(
			self,
			url: str,
			method: str,
			params: Optional[dict[str, Any]] = None,
			json: Optional[dict[str, Any]] = None,
	):
		"""Выполнение запроса в сторонее API"""
		async with aiohttp.request(
				method=method, url=url, params=params, json=json
		) as response:
			try:
				body = await response.json()
			except (aiohttp.ContentTypeError, ValueError):
				body = None
				logger.exception(f"Bad request")
		return body

	async def user_info(self, user: UserSettings):
		"""Получение данных пользователя из стороннего API"""
		user_data = await self.make_request(self.USER_DATA_URL, method="post", json={"user_id": str(user.id)})
		return user_data

	async def film_info(self, film_id: str):
		"""Получение данных о фильме из стороннего API"""
		film_data = await self.make_request(self.FILM_DATA_URL, method="post", json={"user_id": film_id})
		return film_data


@lru_cache
def get_request_service() -> RequestService:
	return RequestService()
