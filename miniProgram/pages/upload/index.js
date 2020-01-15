// pages/upload/index.js
const app = getApp()
Page({
  data: {
    button_content: "确定并上传",
    button_disabled: false,
    currentScanIndex: 0,
    files: [],
    album_list: [],
    albumIndex: 0,
    album: [],
    upload_list: [],
  },
  bindAlbumChange: function (e) {
    this.setData({
      albumIndex: e.detail.value
    })
  },
  onLoad: function (options) {
    var that = this
    wx.setNavigationBarTitle({
      title: "图片上传"
    })
    app.checkOpenId()
    app.doPost('/album/get', {
      "wechat": app.globalData.openID,
    }).then(function (result) {
      if (result) {
        if (result.error) {
          app.responseAction("相册列表获取失败", result.message)
        } else {
          if (result.message.list_data.length == 0) {
            wx.showModal({
              title: "未获取到相册",
              content: "请新建相册再使用上传功能",
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
          that.setData({
            album_list: result.message.list_data,
            album: result.message.result_data
          })
        }
      } else {
        app.failRequest()
      }
    })
  },
  chooseImage: function (e) {
    var that = this;
    wx.chooseImage({
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        that.setData({
          files: that.data.files.concat(res.tempFilePaths),
          upload_list: that.data.upload_list.concat(res.tempFilePaths)
        });
      }
    })
  },
  uploadImage: function (e) {
    var that = this
    that.setData({
      button_disabled: true,
      button_content: "正在上传，请等待"
    })
    wx.showToast({
      title: '开始上传',
    })
    var that = this
    var cid = this.data.album[this.data.albumIndex].cid
    for (var index in this.data.files) {
      var type = "jpg"
      wx.getImageInfo({
        src: this.data.files[index],
        success: function (res) {
          console.log(res)
          type = res.type
        }
      })
      var url = this.data.files[index]
      that.getBase64(url, cid, type)
    }
  },
  previewImage: function (e) {
    var that = this;
    console.log("ID: ", e.currentTarget.id)
    wx.showActionSheet({
      itemList: ['预览', '删除'],
      success: function (res) {
        if (!res.cancel) {
          if (res.tapIndex == 0) {
            wx.previewImage({
              current: e.currentTarget.id, // 当前显示图片的http链接
              urls: that.data.files // 需要预览的图片http链接列表
            })
          } else {
            that.setData({
              files: that.remove(that.data.files, e.currentTarget.id)
            });
          }
        }
      }

    });
  },
  getIndex: function (array, val) {
    for (var i = 0; i < array.length; i++) {
      if (array[i] == val) {
        return i
      }
    }
    return -1
  },
  remove: function (array, val) {
    for (var i = 0; i < array.length; i++) {
      if (array[i] == val) {
        array.splice(i, 1);
      }
    }
    return array;
  },
  getBase64: function (file, cid, type) {
    var that = this
    wx.getFileSystemManager().readFile({
      filePath: file, //选择图片返回的相对路径
      encoding: 'base64', //编码格式
      success: resultBase => { //成功的回调
        app.doPost('/photo/upload', {
          "wechat": app.globalData.openID,
          "cid": cid,
          "base64": resultBase.data,
          "type": type,
          "index": that.getIndex(that.data.files, file)
        }).then(function (result) {
          if (result) {
            console.log(result)
            if (result.error) {
              var bool = "upload_list[" + result.message.index + "]";
              that.setData({
                [bool]: result.error ? false : true
              })
            } else {
              var bool = "upload_list[" + result.message.index + "]";
              that.setData({
                [bool]: result.error ? false : true
              })
            }
            if (that.ifSuccess(that.data.upload_list) == true) {
              that.setData({
                button_disabled: false,
                button_content: "上传完成，继续上传",
                files: []
              })
              wx.showToast({
                title: '上传完成',
              })
            }
          } else {
            var bool = "upload_list[" + result.message.index + "]";
            that.setData({
              [bool]: result.error ? false : true
            })
          }
        })
      },
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
  },
  ifSuccess: function (inputList) {
    console.log(inputList)
    for (var i = 0; i < inputList.length; i++) {
      if (inputList[i] != true && inputList[i] != false) {
        return false
      }
    }
    return true
  }
})