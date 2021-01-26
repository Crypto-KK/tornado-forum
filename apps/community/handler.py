import os
import uuid

import aiofiles

from apps.community.forms import CommunityGroupForm
from apps.community.service import CommunityGroupService
from forum.handler import BaseHandler
from utils.decorators import authenticated_async


class GroupHandler(BaseHandler):

    @authenticated_async
    async def post(self, *args, **kwargs):

        #不能使用jsonform
        group_form = CommunityGroupForm(self.request.body_arguments)
        if group_form.validate():
            #自己完成图片字段的验证
            files_meta = self.request.files.get("front_image", None)
            print(files_meta)
            if not files_meta:
                self.set_400_status()
                self.response(msg="请上传图片")
            else:
                #完成图片保存并将值设置给对应的记录
                #通过aiofiles写文件
                #1. 文件名
                new_filename = ""
                for meta in files_meta:
                    filename = meta['filename']
                    new_filename = f"{uuid.uuid1()}_{filename}"
                    file_path = os.path.join(self.settings["MEDIA_ROOT"], new_filename)
                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(meta['body'])

                group = await CommunityGroupService.instance().create_group(
                    creator=self.current_user,
                    name=group_form.name.data,
                    category=group_form.category.data,
                    desc=group_form.desc.data,
                    notice=group_form.notice.data,
                    front_image=new_filename
                )
                self.response(data={
                    "id": group.id
                }, msg="添加成功")
        else:
            self.set_400_status()
            self.form_invalid_response(group_form, "添加失败")