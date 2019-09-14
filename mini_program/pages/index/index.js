//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: '时光相册',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    album: true
  },
  //事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    
    var that = this
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

  getUserInfo: function(e) {
    app.globalData.testAccount = false
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
    console.log("openID: ", app.globalData.openID)
    console.log("nickName: ", app.globalData.userInfo.nickName)
    const wxreq = wx.request({
      url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/login',
      data: {
        "wechat": app.globalData.openID,
        "nickname": app.globalData.userInfo.nickName,
        "remark": app.globalData.userInfo
      },
      header: {
        "Content-Type": "application/x-www-form-json"
      },
      method: "POST",
      success: (res) => {
        console.log("Success: ", res.data)
        if (res.data.result != true) {
          this.setData({
            userInfo: null,
            hasUserInfo: false
          })
        }else{
          console.log("result is true")
          this.setData({
            hasUserInfo: true
          })
          wx.redirectTo({
            url: '/pages/index_list/index',
          })
        }
      },
      fail: (res) => {
        console.log("Faild: ", res.data)
        this.setData({
          userInfo: null,
          hasUserInfo: false
        })
      }
    })
  },
  getTest: function(){
    app.globalData.testAccount = true
    wx.redirectTo({
      url: '/pages/index_list/index',
    })
  }
})
