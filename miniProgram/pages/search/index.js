// pages/search/index.js
const app = getApp()
Page({
  data: {
    inputShowed: false,
    inputVal: "",
    hot_search_data: [],
    tags: []
  },
  onLoad: function(options) {
    var that = this
    wx.setNavigationBarTitle({
      title: "图片搜索"
    })
    app.checkOpenId()
    app.doPost('/tags/list', {
      "wechat": app.globalData.openID,
    }).then(function (result) {
      if (result) {
        if (result.error) {
          app.responseAction("获取失败", result.message)
        } else {
          console.log(result)
          that.setData({
            tags: result.message.result
          })
        }
      } else {
        app.failRequest()
      }
    })
  },
  showInput: function() {
    this.setData({
      inputShowed: true
    });
  },
  hideInput: function() {
    this.setData({
      inputVal: "",
      inputShowed: false
    });
  },
  clearInput: function() {
    this.setData({
      inputVal: ""
    });
  },
  inputTyping: function(e) {
    this.setData({
      inputVal: e.detail.value
    });
  },
  searching: function(e) {
    wx.redirectTo({
      url: '/pages/list/index?search=' + this.data.inputVal,
    })
    console.log(this.data.inputVal)
  },
  toIndex: function() {
    wx.redirectTo({
      url: '/pages/index_list/index',
    })
  },
  toSearch: function() {
    wx.redirectTo({
      url: '/pages/search/index',
    })
  },
  toUpload: function() {
    wx.redirectTo({
      url: '/pages/upload/index',
    })
  },
  toManage: function() {
    wx.redirectTo({
      url: '/pages/manage/index',
    })
  }
})