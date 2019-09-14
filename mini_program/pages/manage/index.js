// pages/manage/index.js

const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    album_list: [],
    button_lable: "添加相册",
    button_url: "/pages/set_album/index"
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var that = this
    wx.setNavigationBarTitle({
      title: "相册管理"
    })
    if (app.globalData.userInfo == null) {
      if (app.globalData.testAccount == true) {
        that.setData({
          button_lable: "注册账号",
          button_url: "/pages/index/index"
        })
      } else {
        wx.redirectTo({
          url: '/pages/index/index'
        })
      }
    } else {
      wx.request({
        url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/get_album',
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
            album_list: res.data.result_data
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
                wx.redirectTo({
                  url: '/pages/index/index',
                })
              } else {
                console.log('用户点击辅助操作')
                wx.redirectTo({
                  url: '/pages/index/index',
                })
              }
            }
          });
        }
      })
    }
  },

  deleteAlbum: function(res) {
    console.log("cid: ", res.target.dataset.cid)
    wx.request({
      url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/delete_album',
      data: {
        "wechat": app.globalData.openID,
        "cid": res.target.dataset.cid
      },
      header: {
        "Content-Type": "application/json"
      },
      method: "POST",
      success: function(res) {
        console.log("Success: ", res.data)
        if (res.data.result == true) {
          wx.showModal({
            title: "删除成功",
            content: res.data.msg,
            cancelText: "关闭窗口",
            success: function(res) {
              console.log(res);
              if (res.confirm) {
                console.log('用户点击主操作')
                wx.redirectTo({
                  url: '/pages/manage/index',
                })
              } else {
                console.log('用户点击辅助操作')
                wx.redirectTo({
                  url: '/pages/manage/index',
                })
              }
            }
          });
        } else {
          wx.showModal({
            title: "删除失败",
            content: res.data.msg,
            cancelText: "关闭窗口",
            success: function(res) {
              console.log(res);
              if (res.confirm) {
                console.log('用户点击主操作')
              } else {
                console.log('用户点击辅助操作')
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
              wx.redirectTo({
                url: '/pages/index/index',
              })
            } else {
              console.log('用户点击辅助操作')
              wx.redirectTo({
                url: '/pages/index/index',
              })
            }
          }
        });
      }
    })
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