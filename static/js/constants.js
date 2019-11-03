var MYCONST = {};

Object.defineProperty(MYCONST, "blogImage", {
  value: '/static/img/default_blog.jpg',  //该属性本身不受 configurable 的影响，由于属性可写，修改成功
  enumerable: false
});