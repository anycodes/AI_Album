// pages/category/index.js
const app = getApp()
Page({
  data: {
    istrue: false,
    this_pic: "",
    this_msg: "",
    this_pid: "",
    cid: false,
    tags: false,
    search: false,
    name: "图片列表",
    creattime: "",
    creatarea: "",
    remark: "",
    pic: []
  },
  onLoad: function (options) {
    wx.setNavigationBarTitle({
      title: this.data.name
    })
    app.checkOpenId()
    this.setData({
      cid: options.id,
      tags: options.tags,
      search: options.search,
    })
    var that = this
    that.getPageData()
  },
  openGallery: function (res) {
    this.setData({
      istrue: true,
      this_pic: res.target.dataset.imgsrc,
      this_msg: res.target.dataset.imgmsg,
      this_pid: res.target.dataset.imgpid
    })
  },
  closeGallery: function () {
    this.setData({
      istrue: false
    })
  },
  delePic: function (res) {
    var that = this
    app.doPost('/photo/delete', {
      "wechat": app.globalData.openID,
      "pid": res.target.dataset.imgpid
    }).then(function (result) {
      if (result) {
        if (result.error) {
          app.responseAction("删除失败", result.message)
        } else {
          wx.showModal({
            title: "删除成功",
            content: result.message,
            cancelText: "关闭窗口",
          });
          that.getPageData()
        }
      } else {
        app.failRequest()
      }
    })
  },
  getPageData: function () {
    if (this.data.cid) {
      var that = this
      app.doPost('/photo/get', {
        "wechat": app.globalData.openID,
        "cid": that.data.cid
      }).then(function (result) {
        if (result) {
          if (result.error) {
            app.responseAction("获取失败", result.message)
          } else {
            that.setData({
              pic: result.message.pic,
              name: result.message.category.name,
              creattime: result.message.category.creattime,
              creatarea: result.message.category.creatarea,
              remark: result.message.category.remark,
              cid: result.message.category.cid,
            })
          }
        } else {
          app.failRequest()
        }
      })
    } else if (this.data.tags) {
      var that = this
      app.doPost('/photo/get/tags', {
        "wechat": app.globalData.openID,
        "tags": that.data.tags
      }).then(function (result) {
        if (result) {
          if (result.error) {
            app.responseAction("获取失败", result.message)
          } else {
            that.setData({
              pic: result.message.pic,
              name: that.data.tags,
              creatarea: "标签",
              creattime: that.data.tags,
              remark: "通过标签查询到的图片列表",
            })
          }
        } else {
          app.failRequest()
        }
      })
    } else if (this.data.search) {
      var that = this
      app.doPost('/photo/get/search', {
        "wechat": app.globalData.openID,
        "search": that.data.search
      }).then(function (result) {
        if (result) {
          if (result.error) {
            app.responseAction("获取失败", result.message)
          } else {
            that.setData({
              pic: result.message.pic,
              name: "搜索结果",
              creatarea: "智能",
              creattime: "检索",
              remark: that.data.search,
            })
          }
        } else {
          app.failRequest()
        }
      })
    }
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