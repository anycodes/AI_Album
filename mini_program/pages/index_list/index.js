//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    'motto': '时光相册',
    'categoryList': [],
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function(options) {

    var that = this

    wx.setNavigationBarTitle({
      title: "相册列表"
    })

    console.log(app.globalData.userInfo)
    if (app.globalData.userInfo == null) {
      if(app.globalData.testAccount == true){
      }else{
        wx.redirectTo({
          url: '/pages/index/index'
        })
      }
    } else {
      wx.request({
        url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/get_album?time=1',
        data: {
          "wechat": app.globalData.openID,
        },
        header: {
          "Content-Type": "application/json"
        },
        method: "POST",
        success: function(res) {
          console.log("Success: ", res.data)
          that.setData({
            categoryList: res.data.result_data
          })
        },
        fail: function(res) {
          console.log("Faild: ", res.data)
          wx.showModal({
            title: "操作失败",
            content: "请检查网络设置",
            cancelText: "关闭窗口",
            success: function(res) {
              console.log(res);
              if (res.confirm) {
                console.log('用户点击主操作')
                // wx.redirectTo({
                //   url: '/pages/index/index',
                // })
              } else {
                console.log('用户点击辅助操作')
                // wx.redirectTo({
                //   url: '/pages/index/index',
                // })
              }
            }
          });
        }
      })
    }
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