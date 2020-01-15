//index.js
const app = getApp()
Page({
  data: {
    motto: '时光相册',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    album: true
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      wx.redirectTo({
        url: '/pages/index_list/index',
      })
    } else if (this.data.canIUse) {
      app.userInfoReadyCallback = res => {
        wx.redirectTo({
          url: '/pages/index_list/index',
        })
      }
    } else {
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          wx.redirectTo({
            url: '/pages/index_list/index',
          })
        }
      })
    }
  },
  getUserInfo: function (e) {
    const that = this
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
    app.doPost('/login', {
      "wechat": app.globalData.openID,
      "nickname": app.globalData.userInfo.nickName,
      "remark": app.globalData.userInfo
    }).then(function (result) {
      if (result) {
        if (result.error) {
          that.setData({
            userInfo: null,
            hasUserInfo: false
          })
        } else {
          that.setData({
            hasUserInfo: true
          })
          wx.redirectTo({
            url: '/pages/index_list/index',
          })
        }
      } else {
        that.setData({
          userInfo: null,
          hasUserInfo: false
        })
      }
    })
  }
})