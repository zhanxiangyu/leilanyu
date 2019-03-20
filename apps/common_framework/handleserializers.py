# -*- coding: utf-8 -*-


class ChangeSerializerFields(object):
    """
    动态修改fields里面的内容 显示查看文档 http://www.django-rest-framework.org/api-guide/serializers/#example
    """
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(ChangeSerializerFields, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
