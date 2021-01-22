from forum.service import BaseService
from apps.users.models import User


class UserService(BaseService):
    model = User

    async def get_user_by_mobile(self, mobile: str) -> User:
        user: User = await self.find_one(mobile=mobile)
        return user

    async def insert_user(self, mobile: str, password: str) -> User:
        user: User = await self.insert(mobile=mobile, password=password)
        return user
