//index.js
const app = getApp()
Page({
  data: {
    'motto': '时光相册',
    'categoryList': [],
  },
  onLoad: function (options) {
    var that = this
    wx.setNavigationBarTitle({
      title: "相册列表"
    })
    app.checkOpenId()
    app.doPost("/album/get", {
      "wechat": app.globalData.openID,
    }).then(function (result) {
      if (result) {
        if (result.error) {
          app.responseAction("获取失败", result.message)
        } else {
          that.setData({
            categoryList: result.message.result_data
          })
        }
      } else {
        app.failRequest()
      }
    })
  },
  toIndex: function () {
    wx.redirectTo({
      url: '/pages/index_list/index',
    })
  },
  toSearch: function () {
    wx.redirectTo({
      url: '/pages/search/index',
    })
  },
  toUpload: function () {
    wx.redirectTo({
      url: '/pages/upload/index',
    })
  },
  toManage: function () {
    wx.redirectTo({
      url: '/pages/manage/index',
    })
  }
})