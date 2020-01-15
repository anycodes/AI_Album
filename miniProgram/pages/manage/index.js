// pages/manage/index.js
const app = getApp()
Page({
  data: {
    album_list: [],
    button_lable: "添加相册",
    button_url: "/pages/set_album/index"
  },
  onLoad: function (options) {
    var that = this
    wx.setNavigationBarTitle({
      title: "相册管理"
    })
    app.checkOpenId()
    app.doPost('/album/get', {
      "wechat": app.globalData.openID,
    }).then(function (result) {
      if (result) {
        if (result.error) {
          app.responseAction("相册列表获取失败", result.message)
        } else {
          that.setData({
            album_list: result.message.result_data
          })
        }
      } else {
        app.failRequest()
      }
    })
  },
  deleteAlbum: function (res) {
    app.doPost('/album/delete', {
      "wechat": app.globalData.openID,
      "cid": res.target.dataset.cid
    }).then(function (result) {
      if (result) {
        if (result.error) {
          app.responseAction("删除失败", result.message)
        } else {
          wx.showModal({
            title: "删除成功",
            content: result.message,
            cancelText: "关闭窗口",
            success: function (res) {
              if (res.confirm) {
                wx.redirectTo({
                  url: "/pages/manage/index",
                })
              } else {
              }
            }
          });
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