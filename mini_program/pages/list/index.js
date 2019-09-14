// pages/category/index.js

const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
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

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {

    wx.setNavigationBarTitle({
      title: this.data.name
    })

    if (app.globalData.userInfo == null) {
      wx.redirectTo({
        url: '/pages/index/index'
      })
    }

    this.setData({
      cid: options.id,
      tags: options.tags,
      search: options.search,
    })

    var that = this
    that.getPageData()

  },

  openGallery: function(res) {
    console.log(res)
    // var imgsrc = res.target.dataset.imgsrc;
    // console.log(imgsrc)
    this.setData({
      istrue: true,
      this_pic: res.target.dataset.imgsrc,
      this_msg: res.target.dataset.imgmsg,
      this_pid: res.target.dataset.imgpid
    })
  },
  closeGallery: function() {
    this.setData({
      istrue: false
    })
  },
  delePic: function(res) {
    var that = this
    console.log(res.target.dataset.imgpid)
    wx.request({
      url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/delete_photo',
      data: {
        "wechat": app.globalData.openID,
        "pid": res.target.dataset.imgpid
      },
      header: {
        "Content-Type": "application/json"
      },
      method: "POST",
      success: function(res) {
        console.log("Success: ", res.data)
        if (res.data.result == true) {
          console.log(getCurrentPages())
          wx.showModal({
            title: "删除成功",
            content: res.data.msg,
            cancelText: "关闭窗口",
            success: function(res) {
              console.log(res);
            }
          });
          that.getPageData()
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
  getPageData: function() {
    if (this.data.cid) {
      var that = this
      console.log("cid: ", this.data.cid)
      wx.request({
        url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/get_photo',
        data: {
          "wechat": app.globalData.openID,
          "cid": that.data.cid
        },
        header: {
          "Content-Type": "application/json"
        },
        method: "POST",
        success: function(res) {
          console.log("Success: ", res.data)
          if (res.data.result == false) {
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
          } else {
            that.setData({
              pic: res.data.result.pic,
              name: res.data.result.category.name,
              creattime: res.data.result.category.creattime,
              creatarea: res.data.result.category.creatarea,
              remark: res.data.result.category.remark,
              cid: res.data.result.category.cid,
            })
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
    } else if (this.data.tags) {
      var that = this
      console.log("tags: ", this.data.tags)
      wx.request({
        url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/get_photo_tags',
        data: {
          "wechat": app.globalData.openID,
          "tags": that.data.tags
        },
        header: {
          "Content-Type": "application/json"
        },
        method: "POST",
        success: function(res) {
          console.log("Success: ", res.data)
          if (res.data.result == false) {
            wx.showModal({
              title: "获取失败",
              content: res.data.msg,
              cancelText: "关闭窗口",
              success: function(res) {
                console.log(res);
                if (res.confirm) {
                  console.log('用户点击主操作')
                  wx.redirectTo({
                    url: '/pages/search/index',
                  })
                } else {
                  console.log('用户点击辅助操作')
                  wx.redirectTo({
                    url: '/pages/search/index',
                  })
                }
              }
            });
          } else {
            that.setData({
              pic: res.data.result.pic,
              name: that.data.tags,
              creatarea: "标签",
              creattime: that.data.tags,
              remark: "通过标签查询到的图片列表",
            })
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
                  url: '/pages/search/index',
                })
              } else {
                console.log('用户点击辅助操作')
                wx.redirectTo({
                  url: '/pages/search/index',
                })
              }
            }
          });
        }
      })
    } else if (this.data.search) {
      var that = this
      console.log("search: ", this.data.search)
      wx.request({
        url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/get_photo_search',
        data: {
          "wechat": app.globalData.openID,
          "search": that.data.search
        },
        header: {
          "Content-Type": "application/json"
        },
        method: "POST",
        success: function(res) {
          console.log("Success: ", res.data)
          if (res.data.result == false) {
            wx.showModal({
              title: "获取失败",
              content: res.data.msg,
              cancelText: "关闭窗口",
              success: function(res) {
                console.log(res);
                if (res.confirm) {
                  console.log('用户点击主操作')
                  wx.redirectTo({
                    url: '/pages/search/index',
                  })
                } else {
                  console.log('用户点击辅助操作')
                  wx.redirectTo({
                    url: '/pages/search/index',
                  })
                }
              }
            });
          } else {
            that.setData({
              pic: res.data.result.pic,
              name: "搜索结果",
              creatarea: "智能",
              creattime: "检索",
              remark: that.data.search,
            })
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
                  url: '/pages/search/index',
                })
              } else {
                console.log('用户点击辅助操作')
                wx.redirectTo({
                  url: '/pages/search/index',
                })
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