// pages/search/index.js

const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    inputShowed: false,
    inputVal: "",
    hot_search_data: [],
    tags: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var that = this
    wx.setNavigationBarTitle({
      title: "图片搜索"
    })
    if (app.globalData.userInfo == null) {
      if (app.globalData.testAccount == true) {
      } else {
        wx.redirectTo({
          url: '/pages/index/index'
        })
      }
    } else {
      wx.request({
        url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/tags_list',
        data: {
          "wechat": app.globalData.openID,
        },
        header: {
          "Content-Type": "application/json"
        },
        method: "POST",
        success: function(res) {
          console.log("Success: ", res.data)
          if (res.data.msg == "查询成功") {
            that.setData({
              tags: res.data.result
            })
          } else {
            wx.showModal({
              title: "获取失败",
              content: res.data.msg,
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