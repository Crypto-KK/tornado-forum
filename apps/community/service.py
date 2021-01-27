from apps.community.models import CommunityGroup
from forum.service import BaseService


class CommunityGroupService(BaseService):
    model = CommunityGroup

    async def create_group(self, **kwargs) -> CommunityGroup:
        g: CommunityGroup = await self.insert(**kwargs)
        return g

