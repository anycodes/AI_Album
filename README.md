

# AI_Album说明
## 项目背景

![avatar](https://github.com/anycodes/album/blob/master/image/01.png?raw=true)

在日常生活中，我们经常会遇到搜索照片的情况，尤其是对寻找过去很久的图片，记忆中仅剩下零散的记忆的时候，我们检索照片的方法通常是定位到大致的时间，然后一张一张的去查看，但是这种做法效率低下，还经常会漏掉我们的目标图片，所以这个时候，就迫切需要一款可以搜索图片的软件，即我们可以通过简单的文字描述，实现图片的快速检索。
近几年微信小程序的发展速度飞快，从2017年年初，张小龙在2017微信公开课Pro上发布的小程序正式上线到目前为止，小程序已经覆盖了超过200个细分行业，服务超过1000亿人次用户，年交易增长超过600%，创造超过5000亿的商业价值。而小程序蓬勃发展的背后，是一群优秀的小程序开发者的不断贡献。
本实例将会通过微信小程序，在Serverless架构上，实现一款基于人工智能的相册小工具，该款小工具可以在保证基础相册功能（新建相册、删除相册、上传图片、查看图片、删除图片）的基础上，增加搜索功能，即用户上传图片之后，基于Image Caption技术，自动对图片进行描述，实现Image to Text的过程，当用户进行搜索时，通过文本间的相似度，返回给用户最贴近的图片。


## 项目设计
该项目设计主要包括三部分，分别是功能设计，模块设计以及数据库设计，其中功能设计主要是每个功能点的定义，模块设计主要是后端所需要的各个功能模块的设计，数据库设计表示的是数据库的整体结构和形式。

## 功能设计	
在这一部分，主要拥有登录功能、相册新建、图片上传以及相关预览功能，以及搜索功能，整体如图所示。

![avatar](https://github.com/anycodes/album/blob/master/image/61.png?raw=true)

其中注册功能的主要作用是，通过获取用户的唯一Id（微信中的OpenId），来讲用户信息存储到数据库中，之后的所有操作，都需要根据该Id作为区分。相册功能主要包括相册添加、修改、删除以及查看等功能。图片功能包括图片上传功能、删除功能、查看功能。搜索功能主要是可以查看指定标签对应的图片列表，以及指定搜索内容对应的列表。当然这四个主要功能和模块是和前端关系紧密的部分，除此之外还有后端异步操作的两个模块，分别是图像压缩功能以及图像描述功能。
### 注册功能：
注册功能主要是用户点击注册账号之后，执行的动作。该动作需要注意，用户点击注册账号注册的时候要先判断用户是否已经注册过，如果已经注册过则默认登陆，否则进行注册并登陆。当用户不想注册时，可以点击体验程序，可以对程序大部分页面进行预览。但是不能实现有关数据库的增删改查等功能。登录功能页面如图所示。

 ![avatar](https://github.com/anycodes/album/blob/master/image/62.png?raw=true)

### 相册功能：
当用户注册登录之后，可以在相册管理页面进行相册相关的管理，包括编辑功能，删除功能以及新建功能，此处在进行添加和修改的时候，需要注意相册名称是否已经存在；在进行删除相册，修改相册等操作时要判断用户是否有操作该相册的权限等，如图所示，是相册功能相关原型图。

![avatar](https://github.com/anycodes/album/blob/master/image/63.png?raw=true)

### 图片功能：
图片功能主要包括图片列表以及图片获取、图片删除以及图片上传功能，在图片获取与删除的过程中，要对用户是否有该项操作的权限进行判断，图片上传时也要判断用户是否有上传到指定相册的权限。图片功能相关原型图如所示。

![avatar](https://github.com/anycodes/album/blob/master/image/64.png?raw=true)     

图片功能部分除了用户侧可见的功能，还有定时任务，当用户上传图片之后，系统会在后台异步进行图像压缩以及图像的描述，关键词提取等。整体流程如图所示。

 ![avatar](https://github.com/anycodes/album/blob/master/image/65.png?raw=true)

### 搜索功能：
搜索功能指的是通过关键词或者使用者的描述，可以获得到目标数据的过程，这一功能原型图如图所示。

 ![avatar](https://github.com/anycodes/album/blob/master/image/66.png?raw=true)

这一部分的难点和重点在于通过用户的描述，搜索到目标数据的过程。这个过程的基本流程如图所示。

 ![avatar](https://github.com/anycodes/album/blob/master/image/67.png?raw=true)


## 数据库建立

 ![avatar](https://github.com/anycodes/album/blob/master/image/mysql.png?raw=true)

数据库部分主要对相关的表和表之间的关系进行建立。
首先需要创建项目所必须的表：
```mysql

CREATE DATABASE `album`;
CREATE TABLE `album`.`tags` ( `tid` INT NOT NULL AUTO_INCREMENT , `name` VARCHAR(255) NOT NULL , `remark` TEXT NULL , PRIMARY KEY (`tid`)) ENGINE = InnoDB;
CREATE TABLE `album`.`category` ( `cid` INT NOT NULL AUTO_INCREMENT , `name` VARCHAR(255) NOT NULL , `sorted` INT NOT NULL DEFAULT '1' , `user` INT NOT NULL , `remark` TEXT NULL , `publish` DATE NOT NULL , `area` VARCHAR(255) NULL , PRIMARY KEY (`cid`)) ENGINE = InnoDB;
CREATE TABLE `album`.`users` ( `uid` INT NOT NULL AUTO_INCREMENT , `nickname` TEXT NOT NULL , `wechat` VARCHAR(255) NOT NULL , `remark` TEXT NULL , PRIMARY KEY (`uid`)) ENGINE = InnoDB;
CREATE TABLE `album`.`photo` ( `pid` INT NOT NULL AUTO_INCREMENT , `name` VARCHAR(255) NOT NULL , `small` VARCHAR(255) NOT NULL , `large` VARCHAR(255) NOT NULL , `category` INT NOT NULL , `tags` VARCHAR(255) NULL , `remark` TEXT NULL , `creattime` DATE NOT NULL , `creatarea` VARCHAR(255) NOT NULL , `user` INT NOT NULL ,  PRIMARY KEY (`pid`)) ENGINE = InnoDB;
CREATE TABLE `album`.`photo_tags` ( `ptid` INT NOT NULL AUTO_INCREMENT , `tag` INT NOT NULL , `photo` INT NOT NULL , `remark` INT NULL , PRIMARY KEY (`ptid`)) ENGINE = InnoDB;

```
创建之后，逐步添加表之间的关系以及部分限制条件：
```mysql

ALTER TABLE `photo_tags` ADD CONSTRAINT `photo_tags_tags_alter` FOREIGN KEY (`tag`) REFERENCES `tags`(`tid`) ON DELETE CASCADE ON UPDATE RESTRICT; 
ALTER TABLE `photo_tags` ADD CONSTRAINT `photo_tags_photo_alter` FOREIGN KEY (`photo`) REFERENCES `photo`(`pid`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `photo` ADD CONSTRAINT `photo_category_alter` FOREIGN KEY (`category`) REFERENCES `category`(`cid`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `photo` ADD CONSTRAINT `photo_user_alter` FOREIGN KEY (`user`) REFERENCES `users`(`uid`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `category` ADD CONSTRAINT `category_user_alter` FOREIGN KEY (`user`) REFERENCES `users`(`uid`) ON DELETE CASCADE ON UPDATE RESTRICT;
ALTER TABLE `tags` ADD unique(`name`);

```
## 使用方法

* 在使用之前您需要有一个腾讯云的账号，并且开通了COS、COS、APIGW以及CDB等相关产品权限；
* 将项目clone到本地，配置自己的密钥信息、数据库信息。配置文件在`cloudFunction`目录下的`serverless.yaml`中：
```yaml
# 函数们的整体配置信息
Conf:
  component: "serverless-global"
  inputs:
    region: ap-shanghai
    runtime: Python3.6
    handler: index.main_handler
    include_common: ./common
    mysql_host: gz-c************************.com
    mysql_user: root
    mysql_password: S************************!
    mysql_port: 6************************0
    mysql_db: album
    mini_program_app_id: asdsa************************dddd
    mini_program_app_secret: fd340c4************************8744ee
    tencent_secret_id: AKID1y************************l1q0kK
    tencent_secret_key: cCoJ************************FZj5Oa
    tencent_appid: 1256773370
    cos_bucket: 'album-1256773370'
    domain: album.0duzahn.com
```
由于我目前使用的是Serverless Components，没有全局变量等，所以在此处增加了全局变量组件，在这里设置好全局变量，在之后的Components中可以直接引用，例如：
```yaml
# 创建存储桶
CosBucket:
  component: '@serverless/tencent-website'
  inputs:
    code:
      src: ./cos
    region:  ${Conf.region}
    bucketName: ${Conf.cos_bucket}
```
* 安装必备工具，例如必须要安装Serverless Framework（可以参考：https://cloud.tencent.com/document/product/1154/39005）, 同样由于本项目后台开发语言是Python，您也需要一些Python的开发工具以及包管理工具，以及小程序云开发的IDE；
* 在部分文件夹下安装相对应的依赖：
    * `cloudFunction/album/prdiction`需要安装Pillow, opencv，tensorflow，jieba
    * `cloudFunction/album/getPhotoSearch`需要安装gensim，jieba以及collections
    * `cloudFunction/album/compression`需要安装Pillow
  注意，在安装的时候一定要用CentOS操作系统，并且Python要3.6版本，如果没相对应系统，可以在这里打包对应的依赖：http://serverless.0duzhan.com/app/scf_python_package_download/
* 将项目部署到云端，只需要通过指令`serverless --debug`即可：
```text
DEBUG ─ Resolving the template's static variables.
  DEBUG ─ Collecting components from the template.
  DEBUG ─ Downloading any NPM components found in the template.
  DEBUG ─ Analyzing the template's components dependencies.
  DEBUG ─ Creating the template's components graph.
  DEBUG ─ Syncing template state.
  DEBUG ─ Executing the template's components graph.
  DEBUG ─ Starting API-Gateway deployment with name APIService in the ap-shanghai region
 
    ... ...
 
  DEBUG ─ Updating configure... 
  DEBUG ─ Created function Album_Get_Photo_Search successful
  DEBUG ─ Setting tags for function Album_Get_Photo_Search
  DEBUG ─ Creating trigger for function Album_Get_Photo_Search
  DEBUG ─ Deployed function Album_Get_Photo_Search successful
  DEBUG ─ Uploaded package successful /Users/dfounderliu/Documents/code/AIAlbum/.serverless/Album_Prediction.zip
  DEBUG ─ Creating function Album_Prediction
  DEBUG ─ Updating code... 
  DEBUG ─ Updating configure... 
  DEBUG ─ Created function Album_Prediction successful
  DEBUG ─ Setting tags for function Album_Prediction
  DEBUG ─ Creating trigger for function Album_Prediction
  DEBUG ─ Trigger timer: timer not changed
  DEBUG ─ Deployed function Album_Prediction successful

  Conf: 
    region:                  ap-shanghai
      
      ... ...
      
      - 
        path:   /photo/delete
        method: ANY
        apiId:  api-g9u6r9wq
      - 
        path:   /album/delete
        method: ANY
        apiId:  api-b4c4xrq8
      - 
        path:   /album/add
        method: ANY
        apiId:  api-ml6q5koy

  156s › APIService › done

```
例如我的这个过程，只用了156s部署了所有函数，然后打开小程序的id带入`miniProgram`目录，并且填写自己的`appid`在文件`project.config.json`的第17行，同时也要配置自己项目的基础目录，就是API网关给我们返回的地址，写在`app.js`的第10行，此时项目就可以运行起来了。
当然，考虑到部分小伙伴可能比较喜欢方便，所以我这里也提供了后台的压缩包：	https://album-1256773370.cos.ap-shanghai.myqcloud.com/others/AIAlbum.zip