# -*- coding: utf-8 -*-

from haystack.views import SearchView

from .models import Blog


class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        # blogs = Blog.objects.all()
        # context["blogs"] = blogs
        return context
