
Vue.filter('formatdate', function (value) {
    return format(value, 'yyyy-mm-dd HH-mm-ss')
});