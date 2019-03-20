# -*- coding: utf-8 -*-
from rest_framework.response import Response


class ListMixin(object):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = self.extra_handle_list_data(serializer.data)
        return Response(data)

    def extra_handle_list_data(self, data):
        return data
