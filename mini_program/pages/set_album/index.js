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
  bindText: function(e) {
    console.log(e)
    this.setData({
      remark: e.detail.value
    })
  },
  bindArea: function(e) {
    console.log(e.detail.value)
    this.setData({
      area: e.detail.value
    })
  },
  bindName: function(e) {
    console.log(e.detail.value)
    this.setData({
      name: e.detail.value
    })
  },
  onLoad: function(options) {
    var that = this
    wx.setNavigationBarTitle({
      title: "相册编辑/新增"
    })
    if (app.globalData.userInfo == null) {
      wx.redirectTo({
        url: '/pages/index/index'
      })
    }
    if (options.change) {
      this.setData({
        change: options.change,
        cid: options.cid
      })
      console.log(this.data.change, this.data.cid)
      if (this.data.change != false) {
        wx.request({
          url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/get_album_infor',
          data: {
            "wechat": app.globalData.openID,
            "cid": this.data.cid
          },
          header: {
            "Content-Type": "application/x-www-form-json"
          },
          method: "POST",
          success: function(res) {
            console.log("Success: ", res.data)
            that.setData({
              name: res.data.name,
              area: res.data.creatarea,
              remark: res.data.remark,
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
    }
  },
  bindButton: function() {
    var that = this; //把this对象复制到临时变量that
    console.log(app.globalData.openID, this.data.name, this.data.remark, this.data.area)
    console.log(this.data.change)
    var url
    var data
    if (this.data.change == false) {
      url = 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/add_album'
      data = {
        "wechat": app.globalData.openID,
        "name": this.data.name,
        "sorted": 0,
        "remark": this.data.remark,
        "area": this.data.area
      }
    } else {
      url = 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/change_album'
      data = {
        "wechat": app.globalData.openID,
        "name": this.data.name,
        "sorted": 0,
        "remark": this.data.remark,
        "area": this.data.area,
        "cid": this.data.cid
      }
    }
    const wxreq = wx.request({
      url: url,
      data: data,
      header: {
        "Content-Type": "application/x-www-form-json"
      },
      method: "POST",
      success: function(res) {
        console.log("Success: ", res.data)
        if (res.data.result == true) {
          wx.showModal({
            title: "操作成功",
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
            title: "操作失败",
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