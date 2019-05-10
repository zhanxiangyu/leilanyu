
var initFromBaseModules = function(baseModules){
    return $.extend.apply({}, [true].concat(baseModules || []))
}

var codeUtil = (function (baseModules) {
  var mod = initFromBaseModules(baseModules);

  // Html编码获取Html转义实体
  mod.htmlEncode = function (value) {
    return $('<div/>').text(value).html();
  }

  // Html解码获取Html实体
  mod.htmlDecode = function (value) {
    return $('<div/>').html(value).text();
  }


  mod.htmlEncodeData = function (dataList, fields) {
    $.each(dataList, function (i, data) {
      $.each(fields, function (j, field) {
        data[field] = mod.htmlEncode(data[field]);
      });
    });
  }

  return mod;
}());