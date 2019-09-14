//app.js

App({
  onLaunch: function() {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    wx.login({
      success: function(res) {
        if (res.code) {
          console.log("res: " + res.code)
          wx.request({
            url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/get_openid',
            data: {
              code: res.code,
            },
            header: {
              "Content-Type": "application/x-www-form-json"
            },
            method: 'POST',
            success: function(res) {
              console.log('Success_1:', res)
              var data = res.data.openid
              console.log(data)
              if(data){
                getApp().globalData.openID = data
                wx.getUserInfo({
                  success: function (res) {
                    console.log('Success_2:', res)
                  }
                })
              }else{
                console.log('Faild', res)
              }
            },
            fail: function(res) {
              console.log('Faild', res)
            }
          })
        } else {
          console.log('获取用户登录态失败！' + res.errMsg)
        }
      }

    });

    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              console.log(res)
              this.globalData.userInfo = res.userInfo
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  globalData: {
    userInfo: null,
    userAuth: false,
    testAccount: false,
    openID: null
  }
})