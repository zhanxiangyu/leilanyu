# -*- coding: utf-8 -*-
from django.shortcuts import render


from .models import Comment


# 显示所有评论
# comment_tree = {}
# comment_dict = {}
# comment_request = {}
# for value in comments.json()["rows"]:
#     if value['parent'] != None:
#         parent_id = value['parent']
#         comment_tree.setdefault(parent_id, []).append(value)
#     else:
#         parent_id = value['id']
#         comment_dict[parent_id] = value
# for k, v in comment_dict.items():
#     comment_request.setdefault(k, []).append(v)
# for k, v in comment_tree.items():
#     comment_request.setdefault(k, []).append(v)