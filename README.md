

# AI_Album说明
## 项目背景

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
CREATE TABLE `album`.`photo` ( `pid` INT NOT NULL AUTO_INCREMENT , `name` VARCHAR(255) NOT NULL , `small` VARCHAR(255) NOT NULL , `large` VARCHAR(255) NOT NULL , `category` INT NOT NULL , `tags` VARCHAR(255) NULL , `remark` TEXT NULL , `creattime` DATE NOT NULL , `creatarea` VARCHAR(255) NOT NULL , , `user` INT NOT NULL ,  PRIMARY KEY (`pid`)) ENGINE = InnoDB;
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
## 注意事项
使用本代码的时候需要您注册微信小程序，腾讯云，拿到微信小程序AppID，AppSecret，腾讯云SecretId，SecretKey以及自己的数据库账号密码等信息。

然后修改：

```mini_program/project.config.json ```第17行appid切换为自己微信小程序账号的appid

scf目录下所有的数据库账号密码，需要自己替换为自己的数据库账号密码

```scf/get_openid/get_openid.py```目录中修改自己的APPID和APPSecret
