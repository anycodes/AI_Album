//app.js

App({
  globalData: {
    userInfo: null,
    userAuth: false,
    openID: null
  },

  BaseUrl: 'http://service-ddtipdt5-1256773370.sh.apigw.tencentcs.com/release',

  doPost(uri, data) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: this.BaseUrl + uri,
        data: data,
        header: {
          "Content-Type": "application/x-www-form-json"
        },
        method: "POST",
        success: function (res) {
          resolve(res.data)
        },
        fail: function (res) {
          resolve(null)
        }
      })
    })
  },

  responseAction(title, content) {
    wx.showModal({
      title: title,
      content: content,
      cancelText: "关闭窗口",
      success: function (res) {
        if (res.confirm) {
        } else {
        }
      }
    });
  },

  failRequest() {
    wx.showModal({
      title: "操作失败",
      content: "请检查网络设置",
      cancelText: "关闭窗口",
      success: function (res) {
        if (res.confirm) {} else {}
      }
    });
  },

  checkOpenId() {
    if (!this.globalData.openID) {
      wx.redirectTo({
        url: '/pages/index/index',
      })
    }
  },

  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    wx.login({
      success: function (res) {
        if (res.code) {
          console.log("res: " + res.code)
          wx.request({
            url: "http://service-ddtipdt5-1256773370.sh.apigw.tencentcs.com/release/openid/get",
            data: {
              code: res.code,
            },
            header: {
              "Content-Type": "application/x-www-form-json"
            },
            method: 'POST',
            success: function (res) {
              console.log('Success:', res)
              if (res.error != false) {
                var data = res.data.message.openid
                console.log(data)
                getApp().globalData.openID = data
                wx.getUserInfo({
                  success: function (res) {
                    console.log('Success:', res)
                  }
                })
              } else {
                console.log('Faild', res.data.message)
              }
            },
            fail: function (res) {
              console.log('Faild', res.errMsg)
            }
          })
        } else {
          console.log('获取用户登录态失败！' + res)
        }
      }

    });

    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          wx.getUserInfo({
            success: res => {
              console.log(res)
              this.globalData.userInfo = res.userInfo
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  }
})