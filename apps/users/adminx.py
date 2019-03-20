# -*- coding: utf-8 -*-
import xadmin
from xadmin import views  # 导入xadmin的views


class BasdSetting(object):  # 主题管理器
    enable_themes = True  # 使用主题
    use_bootswatch = True


class GlobalSettings(object):  # 头部系统名称和底部版权管理器
    site_title = '累兰羽博客系统'  # 头部系统名称
    site_footer = '累兰羽'  # 底部版权
    menu_style = 'accordion'  # 设置数据管理导航折叠，以每一个app为一个折叠框
    apps_icons = {
        'blog': 'fa fa-fighter-jet',
        'comments': 'fa fa-fighter-jet',
    }


xadmin.site.register(views.CommAdminView, GlobalSettings)  # 头部系统名称和底部版权管理器绑定views.CommAdminView注册
xadmin.site.register(views.BaseAdminView, BasdSetting)  # 将主题管理器绑定views.BaseAdminView注册
