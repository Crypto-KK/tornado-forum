
from forum.handler import BaseHandler
from utils.decorators import authenticated_async


class GroupHandler(BaseHandler):

    @authenticated_async
    async def get(self):
        return {}
