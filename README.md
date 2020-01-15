# AI_Album说明

## 项目背景



在日常生活中，我们经常会遇到搜索照片的情况，尤其是对寻找过去很久的图片，记忆中仅剩下零散的记忆的时候，我们检索照片的方法通常是定位到大致的时间，然后一张一张的去查看，但是这种做法效率低下，还经常会漏掉我们的目标图片，所以这个时候，就迫切需要一款可以搜索图片的软件，即我们可以通过简单的文字描述，实现图片的快速检索。
近几年微信小程序的发展速度飞快，从2017年年初，张小龙在2017微信公开课Pro上发布的小程序正式上线到目前为止，小程序已经覆盖了超过200个细分行业，服务超过1000亿人次用户，年交易增长超过600%，创造超过5000亿的商业价值。而小程序蓬勃发展的背后，是一群优秀的小程序开发者的不断贡献。
本实例将会通过微信小程序，在Serverless架构上，实现一款基于人工智能的相册小工具，该款小工具可以在保证基础相册功能（新建相册、删除相册、上传图片、查看图片、删除图片）的基础上，增加搜索功能，即用户上传图片之后，基于Image Caption技术，自动对图片进行描述，实现Image to Text的过程，当用户进行搜索时，通过文本间的相似度，返回给用户最贴近的图片。


## 基础设计

<div align=center><img src="https://github.com/anycodes/album/blob/master/image/01.png?raw=true"/></div>

该项目设计主要拥有登录功能、相册新建、图片上传以及相关预览功能，以及搜索功能，整体如图所示。

<div align=center><img src="https://github.com/anycodes/album/blob/master/image/61.png?raw=true"/></div>

其中注册功能的主要作用是，通过获取用户的唯一Id（微信中的OpenId），来讲用户信息存储到数据库中，之后的所有操作，都需要根据该Id作为区分。相册功能主要包括相册添加、修改、删除以及查看等功能。图片功能包括图片上传功能、删除功能、查看功能。搜索功能主要是可以查看指定标签对应的图片列表，以及指定搜索内容对应的列表。当然这四个主要功能和模块是和前端关系紧密的部分，除此之外还有后端异步操作的两个模块，分别是图像压缩功能以及图像描述功能。
#### 注册功能：
注册功能主要是用户点击注册账号之后，执行的动作。该动作需要注意，用户点击注册账号注册的时候要先判断用户是否已经注册过，如果已经注册过则默认登陆，否则进行注册并登陆。当用户不想注册时，可以点击体验程序，可以对程序大部分页面进行预览。但是不能实现有关数据库的增删改查等功能。登录功能页面如图所示。

 <div align=center><img src="https://github.com/anycodes/album/blob/master/image/62.png?raw=true"/></div>

#### 相册功能：
当用户注册登录之后，可以在相册管理页面进行相册相关的管理，包括编辑功能，删除功能以及新建功能，此处在进行添加和修改的时候，需要注意相册名称是否已经存在；在进行删除相册，修改相册等操作时要判断用户是否有操作该相册的权限等，如图所示，是相册功能相关原型图。

<div align=center><img src="https://github.com/anycodes/album/blob/master/image/63.png?raw=true"/></div>

#### 图片功能：
图片功能主要包括图片列表以及图片获取、图片删除以及图片上传功能，在图片获取与删除的过程中，要对用户是否有该项操作的权限进行判断，图片上传时也要判断用户是否有上传到指定相册的权限。图片功能相关原型图如所示。

<div align=center><img src="https://github.com/anycodes/album/blob/master/image/64.png?raw=true"/></div>  

图片功能部分除了用户侧可见的功能，还有定时任务，当用户上传图片之后，系统会在后台异步进行图像压缩以及图像的描述，关键词提取等。整体流程如图所示。

 <div align=center><img src="https://github.com/anycodes/album/blob/master/image/65.png?raw=true"/></div>

#### 搜索功能：
搜索功能指的是通过关键词或者使用者的描述，可以获得到目标数据的过程，这一功能原型图如图所示。

 <div align=center><img src="https://github.com/anycodes/album/blob/master/image/66.png?raw=true"/></div>

这一部分的难点和重点在于通过用户的描述，搜索到目标数据的过程。这个过程的基本流程如图所示。

 <div align=center><img src="https://github.com/anycodes/album/blob/master/image/67.png?raw=true"/></div>


## 开发总结

Serverless架构可以说是目前非常火热的项目，其凭借着按量付费、低成本运维、高效率开发等众多优点于一身，帮助我们的项目快速开发，快速迭代。而Serverless Framework则是一个非常高效的工具，其兼容了AWS，Google Cloud以及腾讯云等多家厂商的Serverless架构，为开发者提供一个多云的开发者工具，目前以腾讯云为例，其拥有Plugin和Components两个部分。

这两个部分可以说是个有千秋，具体的大家可以[官方说明](https://cloud.tencent.com/document/product/1154/39005)，或者自己体验一下。我这里我只说几个我觉得很头疼的问题。

* Plugin部署到线上的函数，会自动变更名字，例如我的函数是myFunction，我的服务和阶段是myService-Dev，那么函数部署到线上就是myService-Dev-myFunction，这样的函数名，很可能会让我的函数间调用等部分产生很多不可控因素。例如我现在的环境是Dev，我函数间调用就要写函数名是myService-Dev-myFunction，如果是我的环境是Test，此时就要写myService-Test-myFunction，我始终觉得，我更改环境应该只需要更改配置，而不是更深入的代码逻辑。所以我对Plugin的这个换名字问题很烦躁；
* Plugin也是有优势的，例如他有Invoke、Remove以及部署单个函数的功能，同时Plugin也有全局变量，我觉得这个更像一个开发者工具，我可以开发、部署、调用、查看一些信息、指标以及删除回滚等操作，都可以通过Plugin完成，这点很给力，我喜欢；
* Components可以看作是一个组件集，这里面包括了很多的Components，可以有基础的Components，例如cos、scf、apigateway等，也有一些拓展的Components，例如在cos上拓展出来的website，可以直接部署静态网站等，还有一些框架级的，例如Koa，Express，这些Components说实话，真的蛮方便的，腾讯官方也是有他们的[最佳实践](https://cloud.tencent.com/document/product/1154/39269)
* Components除了刚才所说的支持的产品多，可以部署框架之外，对我来说，最大吸引力在于这个东西，部署到线上的函数名字就是我指定的名字，不会出现额外的东西，这个我非常看重；
* Components相对Plugin在功能上略显单薄，除了部署和删除，再没有其他，例如Plugin的Invoke，Rollback等等一切都没有，同时，我们如果有多个东西要部署，写到了一个Components的yaml上，那么我们每次部署都要部署所有的，如果我们认为，我们只修改了一个函数，并且不想重新部署其他函数从而注释掉其他函数，那么很抱歉告诉你，不行！他会看到你只有一个函数，并且帮你把你注释掉的函数在线上删除；
* Components更多的定义是组件，所以每个组件就是一个东西，所以在Components上面，是没有全局变量这一说法，这点我觉得很坑。

综上所述的几点，就是在除了官方文档的描述之外，我对Plugin和Components的对比，感情真的可谓是错综复杂，也很期待产品策略可以将二者合并，或者功能对齐，否则单用Plugin，功能上是很全面了，但是产品支持不全面，名字变化我真的不能忍（可能很多人都不能忍），单用Components，没有全局变量，没有更多功能，可谓是产品广度变了，便利增加了，但是功能太淡薄了，我对二者的感情，又恨又爱。

经过了长久的思考，我觉得Plugin部署到线上会导致函数名字变化这个问题，我真的不能忍（或许我就是巨蟹座的强迫症吧，哈哈哈），而且，我个人认为，我未必就能需要到更多的功能，例如invoke，例如metrics等。所以我选择了Components来做这个项目。

说到Components做这项目，我就遇到了第一个难题，我的配置文件怎么办？我有很多的配置，我难道要在每个函数中写一遍？

于是，我做了一个新的：[serverless-global](https://www.npmjs.com/package/serverless-global)，是的，这个Components的功能，或者价值就是可以满足我全局变量的需求，例如这样写我的全局变量：
```YAML
Conf:
  component: "serverless-global"
  inputs:
    mysql_host: gz-cdb-mytest.sql.tencentcdb.com
    mysql_user: mytest
    mysql_password: mytest
    mysql_port: 62580
    mysql_db: mytest
    mini_program_app_id: mytest
    mini_program_app_secret: mytest
 ```
在使用的时候，只需要使用`${}`就可以引用，例如：
```YAML
Album_Login:
  component: "@serverless/tencent-scf"
  inputs:
    name: Album_Login
    codeUri: ./album/login
    handler: index.main_handler
    runtime: Python3.6
    region: ap-shanghai
    environment:
      variables:
        mysql_host: ${Conf.mysql_host}
        mysql_port: ${Conf.mysql_port}
        mysql_user: ${Conf.mysql_user}
        mysql_password: ${Conf.mysql_password}
        mysql_db: ${Conf.mysql_db}
```
这样，我就可以很简单轻松加愉快的，将我的配置信息统一提取到了一个配置的地方。另外这里说一下，我为啥要把一些配置信息放在环境变量，而不是统一放在一个配置文件中，因为环境变量在SCF中，会真的打到环境中，也就是说，你可以直接取到，我个人觉得比每次创建实例读取一次配置文件可能要性能好一些，可能只会好几毫秒，但是，我还是觉得这样做是比较优雅的。最主要的是，相比写到代码中和配置到单独的配置文件中，我这样做之后，我可以分享我的代码给别人，可以更好的保护的我的一些敏感信息。反正喜欢一种方法，有一万个理由，不管充分不充分。

写完了这个部分部分，我开始着手写我的第一个函数，注册登录函数。因为这是一个小程序，所以可以认为，注册登录实际上就是拿着用户的openId去数据库查查有没有信息，有信息的话，就执行登录，没有信息的话就insert一下。那么问题来了，我这里要怎么连接我的数据库？之所以有这样的问题，是源自两个因素：

* 我们平时做项目更多时候都不是每次连接一次数据库，很多时候，数据库的连接是可以保持下来的，但是Serverless架构下可以么？或者我们需要去哪里连接数据库呢？
* 传统项目，我们做数据库连接等，是只有一个方法就可以搞定，但是函数中，每个函数都是单独存在的，我们每个函数都要连接一下数据库？

针对问题1，我们来做一个实验，我去腾讯云云函数创建一个test：

<div align=center><img src="https://github.com/anycodes/album/blob/master/image/02.png?raw=true"/></div>

创建之后，我们疯狂点击测试按钮，多次记录运行日志：

第一次
```text
START RequestId: 4facbf59-3787-11ea-8026-52540029942f

Event RequestId: 4facbf59-3787-11ea-8026-52540029942f

11111111

222222222


END RequestId: 4facbf59-3787-11ea-8026-52540029942f

Report RequestId: 4facbf59-3787-11ea-8026-52540029942f Duration:1ms Memory:128MB MaxMemoryUsed:27.3164MB
```

第二次
```text
START RequestId: 7aaf7921-3787-11ea-aba7-525400e4521d

Event RequestId: 7aaf7921-3787-11ea-aba7-525400e4521d

222222222


END RequestId: 7aaf7921-3787-11ea-aba7-525400e4521d

Report RequestId: 7aaf7921-3787-11ea-aba7-525400e4521d Duration:1ms Memory:128MB MaxMemoryUsed:27.1953MB
```
第三次
```text
START RequestId: 742be57a-3787-11ea-b5c5-52540047de0f

Event RequestId: 742be57a-3787-11ea-b5c5-52540047de0f

222222222


END RequestId: 742be57a-3787-11ea-b5c5-52540047de0f

Report RequestId: 742be57a-3787-11ea-b5c5-52540047de0f Duration:1ms Memory:128MB MaxMemoryUsed:27.1953MB
```
第四次
```text
START RequestId: 6faf934b-3787-11ea-8026-52540029942f

Event RequestId: 6faf934b-3787-11ea-8026-52540029942f

222222222


END RequestId: 6faf934b-3787-11ea-8026-52540029942f

Report RequestId: 6faf934b-3787-11ea-8026-52540029942f Duration:1ms Memory:128MB MaxMemoryUsed:27.1953MB
```

发现了什么？我在函数外侧写的`print("11111111")`实际上只出现了一次，也就是说他只运行了一次，而函数内的`print("222222222")`则是出现了多次，确切来说是每次都会出现，函数在创建的时候，会让我们写一个执行方法，例如`index.main_handler`，就是说默认的入口文件就是`index.py`下的`main_handler`方法。通过我们刚才的这个小实验，是不是可以认为，云函数实际上是随着机器或者容器启动同时启动了一个进程（这个时候会走一次外围的一些代码逻辑），然后当函数执行的时候，会走我们指定的方法，当函数执行完，这个容器并不会被马上销毁，而是进入销毁的倒计时，这个时候如果有请求来了，那么很可能复用这个容器，此时就没有容器启动的说法，会直接执行我们的方法。

按照这个逻辑，是不是我们的函数，如果要在我们的方法之外，初始化数据库，就可以保证尽可能少的数据库连接建立，而满足更多的请求呢？换句话说，是不是和容器复用类似，我们就可以复用数据库的连接了？

所以，我这里可以可以这样写我的整个代码（login为例）

```python
# -*- coding: utf8 -*-

import os
import pymysql
import json

connection = pymysql.connect(host=os.environ.get('mysql_host'),
                             user="root",
                             password=os.environ.get('mysql_password'),
                             port=int(62580),
                             db="mini_album",
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=1)

def getUserInfor(connection, wecaht):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        search_stmt = (
            "SELECT * FROM `users` WHERE `wechat`=%s"
        )
        data = (wecaht)
        cursor.execute(search_stmt, data)
        cursor.close()
        result = cursor.fetchall()
        return len(result)
    except Exception as e:
        print("getUserInfor", e)
        try:
            cursor.close()
        except:
            pass
        return False

def addUseerInfor(connection, wecaht, nickname, remark):
    try:
        connection.ping(reconnect=True)
        cursor = connection.cursor()
        insert_stmt = (
            "INSERT INTO users(wechat,nickname,remark) "
            "VALUES (%s,%s,%s)"
        )
        data = (wecaht, nickname, remark)
        cursor.execute(insert_stmt, data)
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print(e)
        try:
            cursor.close()
        except:
            pass
        return False


def main_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    wecaht = body['wechat']
    nickname = body['nickname']
    remark = str(body['remark'])

    if getUserInfor(connection, wecaht) == 0:
        if addUseerInfor(connection, wecaht, nickname, remark):
            result = True
        else:
            result = False
    else:
        result = True

    return {
        "result": result
    }

```

是的，基本需求满足了，但是代码很难看，很恶心啊。

* 这个函数，我要作为小程序的一个接口，那么就要接APIGW，那么我应该怎么赖在本地测试呢？难不成每次都发到线上配置APIGW触发器才能测试，我的天，太恶心了吧！
* 这个函数需要数据库的连接，需要获取用户的信息等，难道别的函数不需要么？如果需要也要每个函数都要重复写这部分代码？或者说，代码的复用应该如何处理呢？是否可以提取公共组件呢？

所以，我这里将这个函数，规范化和完整化：

```python
# -*- coding: utf8 -*-

import json

try:
    import returnCommon
    from mysqlCommon import mysqlCommon
except:
    import common.testCommon

    common.testCommon.setEnv()

    import common.returnCommon as returnCommon
    from common.mysqlCommon import mysqlCommon


mysql = mysqlCommon()


def main_handler(event, context):
    try:
        print(event)

        body = json.loads(event['body'])

        wecaht = body['wechat']
        nickname = body['nickname']
        remark = str(body['remark'])

        if not wecaht:
            return returnCommon.return_msg(True, "请使用微信小程序登陆本页面。")

        if not mysql.getUserInfor(wecaht):
            if not nickname:
                return returnCommon.return_msg(True, "参数异常，请重试。")
            if mysql.addUserInfor(wecaht, nickname, remark):
                return returnCommon.return_msg(False, "注册成功")
            return returnCommon.return_msg(True, "注册失败，请重试。")
        return returnCommon.return_msg(False, "登录成功")
    except Exception as e:
        print(e)
    return returnCommon.return_msg(True, "用户信息异常，请联系管理员处理")

def test():
    event = {
        "requestContext": {
            "serviceId": "service-f94sy04v",
            "path": "/test/{path}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "identity": {
                "secretId": "abdcdxxxxxxxsdfs"
            },
            "sourceIp": "14.17.22.34",
            "stage": "release"
        },
        "headers": {
            "Accept-Language": "en-US,en,cn",
            "Accept": "text/html,application/xml,application/json",
            "Host": "service-3ei3tii4-251000691.ap-guangzhou.apigateway.myqloud.com",
            "User-Agent": "User Agent String"
        },
        "body": json.dumps({
            "wechat": "12345",
            "nickname": "test",
            "remark": "",
        }),
        "pathParameters": {
            "path": "value"
        },
        "queryStringParameters": {
            "foo": "bar"
        },
        "headerParameters": {
            "Refer": "10.0.2.14"
        },
        "stageVariables": {
            "stage": "release"
        },
        "path": "/test/value",
        "queryString": {
            "foo": "bar",
            "bob": "alice"
        },
        "httpMethod": "POST"
    }
    print(main_handler(event, None))


if __name__ == "__main__":
    test()
```
数据库等一些公共组件，统一放在`common`目录下，例如`mysqlCommon.py`(部分):
```python
# -*- coding: utf8 -*-

import os
import random
import pymysql
import datetime

try:
    import cosClient
except:
    import common.cosClient as cosClient


class mysqlCommon:
    def __init__(self):
        self.getConnection({
            "host": os.environ.get('mysql_host'),
            "user": os.environ.get('mysql_user'),
            "port": int(os.environ.get('mysql_port')),
            "db": os.environ.get('mysql_db'),
            "password": os.environ.get('mysql_password')
        })

    def getConnection(self, conf):
        self.connection = pymysql.connect(host=conf['host'],
                                          user=conf['user'],
                                          password=conf['password'],
                                          port=int(conf['port']),
                                          db=conf['db'],
                                          charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          autocommit=1)

    def doAction(self, stmt, data):
        try:
            self.connection.ping(reconnect=True)
            cursor = self.connection.cursor()
            cursor.execute(stmt, data)
            result = cursor
            cursor.close()
            return result
        except Exception as e:
            print(e)
            try:
                cursor.close()
            except:
                pass
            return False

    def addUserInfor(self, wecaht, nickname, remark):
        insert_stmt = (
            "INSERT INTO users(wechat, nickname, remark) "
            "VALUES (%s,%s,%s)"
        )
        data = (wecaht, nickname, remark)
        result = self.doAction(insert_stmt, data)
        return False if result == False else True
       
```

这样做的好处是：

* 我将数据库提取出一个公共组件，便于维护
* 在login函数中，我根据不同的时期（本地开发和线上），我导入不同的模块：
```python
try:
    import cosClient
except:
    import common.cosClient as cosClient
```
这样会更加便利，同时模拟网关，做一个测试方法：
```python
def test():
    event = {
        "requestContext": {
            "serviceId": "service-f94sy04v",
            "path": "/test/{path}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "identity": {
                "secretId": "abdcdxxxxxxxsdfs"
            },
            "sourceIp": "14.17.22.34",
            "stage": "release"
        },
        "headers": {
            "Accept-Language": "en-US,en,cn",
            "Accept": "text/html,application/xml,application/json",
            "Host": "service-3ei3tii4-251000691.ap-guangzhou.apigateway.myqloud.com",
            "User-Agent": "User Agent String"
        },
        "body": json.dumps({
            "wechat": "12345",
            "nickname": "test",
            "remark": "",
        }),
        "pathParameters": {
            "path": "value"
        },
        "queryStringParameters": {
            "foo": "bar"
        },
        "headerParameters": {
            "Refer": "10.0.2.14"
        },
        "stageVariables": {
            "stage": "release"
        },
        "path": "/test/value",
        "queryString": {
            "foo": "bar",
            "bob": "alice"
        },
        "httpMethod": "POST"
    }
    print(main_handler(event, None))
```
增加本地测试时，指定`test()`方法：
```python
if __name__ == "__main__":
    test()
```
这样，线上触发时，会默认执行`main_handler`, 而本地执行，则会通过`test`走入`main_handler`，我们可以边开发，边测试，弄好了再部署到线上。

同时，我们线上获取配置信息是通过获取环境变量，那么我们本地呢？

我们可以在本地执行的时候，先进行这个操作：

```python
# -*- coding: utf8 -*-

import yaml
import os


def setEnv():
    file = open("/Users/dfounderliu/Documents/code/AIAlbum/serverless.yaml", 'r', encoding="utf-8")
    file_data = file.read()
    file.close()

    data = yaml.load(file_data)
    for eveKey, eveValue in data['Conf']['inputs'].items():
        print(eveKey, eveValue)
        os.environ[eveKey] = str(eveValue)

```

这样，我们这个文件就非常完美的，可以线上直接用，也可以本地直接用了！

那么我们的Yaml怎么写？

 <div align=center><img src="https://github.com/anycodes/album/blob/master/image/03.png?raw=true"/></div>
 
 是的，这样我们就可以很简单轻松加愉快的将我们的公共组件库，在部署函数的时候，引入到项目中。
 
 本地长这样：
 
 <div align=center><img src="https://github.com/anycodes/album/blob/master/image/04.png?raw=true"/></div>
 
 线上长这样：
 
 <div align=center><img src="https://github.com/anycodes/album/blob/master/image/05.png?raw=true"/></div>
 
 对于这个项目，完美解决本地调试，线上运行的全兼容问题。
 
 通过上面简单的实验和分析，我们知道了如何制作公共组件库，如何定义Components的全局变量，如何本地调试和线上触发二者兼得，以及在什么地方初始化数据库"性价比较高"，完成了上面的所有部分，就是我们进行各个子功能函数编写的工作了，基本都是数据库的增删改查。此处不再一一描述。编写完函数之后，可以编写我们的小程序端，都弄好了，整体形势这样：
 
  <div align=center><img src="https://github.com/anycodes/album/blob/master/image/06.gif?raw=true"/></div>
 

## 项目开发
### 数据库建立

 <div align=center><img src="https://github.com/anycodes/album/blob/master/image/mysql.png?raw=true"/></div>

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

### 让Code飞起来

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