// pages/set_album/index.js
const app = getApp()
Page({
  data: {
    change: false,
    cid: -1,
    name: "",
    area: "",
    remark: "",
  },
  bindText: function (e) {
    this.setData({
      remark: e.detail.value
    })
  },
  bindArea: function (e) {
    this.setData({
      area: e.detail.value
    })
  },
  bindName: function (e) {
    this.setData({
      name: e.detail.value
    })
  },
  onLoad: function (options) {
    var that = this
    wx.setNavigationBarTitle({
      title: "相册编辑/新增"
    })
    app.checkOpenId()
    if (options.change) {
      this.setData({
        change: options.change,
        cid: options.cid
      })
      if (this.data.change != false) {
        app.doPost('/album/get/info', {
          "wechat": app.globalData.openID,
          "cid": this.data.cid
        }).then(function (result) {
          if (result) {
            if (result.error) {
              app.responseAction("数据获取失败", result.message)
            } else {
              that.setData({
                name: result.message.name,
                area: result.message.creatarea,
                remark: result.message.remark,
              })
            }
          } else {
            app.failRequest()
          }
        })
      }
    }
  },
  bindButton: function () {
    var that = this;
    var uri
    var data
    if (this.data.change == false) {
      uri = '/album/add'
      data = {
        "wechat": app.globalData.openID,
        "name": this.data.name,
        "sorted": 0,
        "remark": this.data.remark,
        "area": this.data.area
      }
    } else {
      uri = '/album/change'
      data = {
        "wechat": app.globalData.openID,
        "name": this.data.name,
        "sorted": 0,
        "remark": this.data.remark,
        "area": this.data.area,
        "cid": this.data.cid
      }
    }
    app.doPost(uri, data).then(function (result) {
      if (result) {
        if (result.error) {
          app.responseAction("操作失败", result.message)
        } else {
          wx.showModal({
            title: "操作成功",
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