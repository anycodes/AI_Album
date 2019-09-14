// pages/upload/index.js

const app = getApp()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    files: [],
    album_list: [],
    albumIndex: 0,
    album: [],
    upload_list: [],
  },
  bindAlbumChange: function(e) {
    console.log('picker country 发生选择改变，携带值为', e.detail.value);
    console.log('picker country 发生选择改变，对应值为', this.data.album[e.detail.value]);
    this.setData({
      albumIndex: e.detail.value
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var that = this
    wx.setNavigationBarTitle({
      title: "图片上传"
    })
    console.log(app.globalData.userInfo)
    if (app.globalData.userInfo == null) {
      if (app.globalData.testAccount == true) {
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
          "Content-Type": "application/x-www-form-json"
        },
        method: "POST",
        success: function(res) {
          console.log("Success: ", res.data)

          if (res.data.list_data.length == 0){
            wx.showModal({
              title: "未获取到相册",
              content: "请新建相册再使用上传功能",
              cancelText: "关闭窗口",
              success: function (res) {
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
          }

          that.setData({
            album_list: res.data.list_data,
            album: res.data.result_data
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
  chooseImage: function(e) {
    var that = this;
    wx.chooseImage({
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function(res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        that.setData({
          files: that.data.files.concat(res.tempFilePaths),
          upload_list: that.data.upload_list.concat(res.tempFilePaths)
        });
        console.log(that.data.files)

      }
    })
  },
  uploadImage: function(e) {
    var that = this
    var cid = this.data.album[this.data.albumIndex].cid

    console.log(this.data.files)
    console.log(cid)
    console.log("upload")
    for (var index in this.data.files) {
      var type = "jpg"
      wx.getImageInfo({
        src: this.data.files[index],
        success: function(res) {
          console.log(res)
          type = res.type
        }
      })
      var url = this.data.files[index]
      console.log("url", url)
      that.getBase64(url, cid, type)

    }
  },
  previewImage: function(e) {
    var that = this;
    console.log("ID: ", e.currentTarget.id)
    wx.showActionSheet({
      itemList: ['预览', '删除'],
      success: function(res) {
        if (!res.cancel) {
          console.log(res.tapIndex)
          if (res.tapIndex == 0) {
            wx.previewImage({
              current: e.currentTarget.id, // 当前显示图片的http链接
              urls: that.data.files // 需要预览的图片http链接列表
            })
          } else {
            console.log(that.data.files)
            console.log(e.currentTarget.id)
            that.setData({
              files: that.remove(that.data.files, e.currentTarget.id)
            });
            console.log(that.data.files)
          }
        }
      }

    });
  },
  getIndex: function(array, val) {
    console.log("array: ", array)
    console.log("val: ", val)
    for (var i = 0; i < array.length; i++) {
      console.log("_array_: ", array[i])
      console.log("_val_: ", val)
      if (array[i] == val) {
        console.log("Bingo")
        return i
      }
    }
    console.log("Error")
    return -1
  },
  remove: function(array, val) {
    for (var i = 0; i < array.length; i++) {
      if (array[i] == val) {
        array.splice(i, 1);
      }
    }
    return array;
  },
  getBase64: function(file, cid, type) {
    var that = this
    wx.getFileSystemManager().readFile({
      filePath: file, //选择图片返回的相对路径
      encoding: 'base64', //编码格式
      success: resultBase => { //成功的回调
        wx.request({
          url: 'https://service-4ea88fc4-1256773370.gz.apigw.tencentcs.com/release/upload',
          data: {
            "wechat": app.globalData.openID,
            "cid": cid,
            "base64": resultBase.data,
            "type": type,
            "index": that.getIndex(that.data.files, file)
          },
          header: {
            "Content-Type": "application/x-www-form-json"
          },
          method: "POST",
          success: function(res) {
            console.log("Success: ", res)
            console.log(that.data.upload_list)
            var bool = "upload_list[" + res.data.index + "]";
            that.setData({
              [bool]: res.data.result
            })
            console.log(that.data.upload_list)
          },
          fail: function(res) {
            console.log("Faild: ", res)
            console.log(that.data.upload_list)
            var bool = "upload_list[" + res.data.index + "]";
            that.setData({
              [bool]: res.data.result
            })
            console.log(that.data.upload_list)
          }
        })
      },
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