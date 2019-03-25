# leilanyu

## 主要开发环境
![](https://img.shields.io/badge/ubuntu-16.04-orange.svg)
![](https://img.shields.io/badge/python-2.7.12-green.svg)
![](https://img.shields.io/badge/django-1.10.8-blue.svg)
![](https://img.shields.io/badge/drf-3.7.7-red.svg)

### 添加查看用户
用户名 test 密码：123456

### 安装包
pip install -r requiremetns.txt -i https://pypi.mirrors.ustc.edu.cn/simple/ </br>
修改数据库连接， 创建表结构
```python
python manage.py makemigrations users blog comments
python manage.py migrate
```
构建索引 python manage.py rebuild_index


### 完成功能
1. 实现文章列表页面， 文章详情页面
2. 项目添加logger日志功能
3. 完成用户评论功能
4. 用户登录注册
5. 首页列表分页功能
6. 获取匿名用户ip功能
7. 全局搜索功能
8. 添加memcached缓存
9. 详情页面优化
10. 后台美化功能

### 正在开发

- 站点分享
- 第三方登录等
- 个人中心




### 前台页面
- 使用前台页面模板
- 使用vue.js项目功能开发
- 取消使用site

[我的网站](http://www.zhanxiangyu.xyz/)
[我的博客](http://blog.csdn.net/qq_34971175)

