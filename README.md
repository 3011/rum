# 前端监控项目 Real User Monitoring

# 接口
### api/get_website_list

|请求地址: /api/get_website_list| 
|-|
|请求方式: GET|
| 简介: 获取网站列表  |
#### 请求参数：
无（默认返回所有网站）

#### 返回参数：
返回JSON示例
```json
{
  "ok": 1,
  "err_type": "",
  "msg": "成功",
  "data": [
    {
      "hostname": "127.0.0.1",
      "create_time": 1660534258057 //创建时间
    },
    {
      "hostname": "google.com",
      "create_time": 1660534464802
    },
    {
      "hostname": "apple.com",
      "create_time": 1660534483271
    },
    {
      "hostname": "localhost",
      "create_time": 1660537905577
    }
  ]
}
```



### api/get_errors

|请求地址: /api/get_errors| 
|-|
|请求方式: GET|
| 简介: 获取网站列表  |

#### 请求参数：

|名称|类型|说明|
|-|-|-|
|hostname|string|必填，指定查询的hostname，例如：google.com|
|time|int|选填，指定查询时间范围，例如：24为查询近24小时|

#### 返回参数：
返回JSON示例
```json
{
  "ok": 1,
  "err_type": "",
  "msg": "成功",
  "data": {
    "js_error": {
      "count": 2,
      "data": [
        {
          "hostname": "apple.com",
          "title": "前端监控系统",
          "url": "https://apple.com/",
          "timestamp": 1960472173899,
          "full_ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
          "browser_name": "chrome",
          "browse_version": "103.0.0.0",
          "os": "",
          "message": "Uncaught TypeError: Cannot set property 'error' of undefined",
          "position": "0:0",
          "stack": "btnClick (http://localhost:8080/:20:39)^HTMLInputElement.onclick (http://localhost:8080/:14:72)",
          "selector": "HTML BODY #container .content INPUT"
        },
        {
          "hostname": "apple.com",
          "title": "前端监控系统",
          "url": "https://apple.com/",
          "timestamp": 1760472173899,
          "full_ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
          "browser_name": "chrome",
          "browse_version": "103.0.0.0",
          "os": "",
          "message": "Uncaught TypeError: Cannot set property 'error' of undefined",
          "position": "0:0",
          "stack": "btnClick (http://localhost:8080/:20:39)^HTMLInputElement.onclick (http://localhost:8080/:14:72)",
          "selector": "HTML BODY #container .content INPUT"
        }
      ]
    },
    "promise_error": {
      "count": 0,
      "data": []
    },
    "resource_error": {
      "count": 0,
      "data": []
    },
    "xhr_error": {
      "count": 0,
      "data": []
    },
    "white_screen_error": {
      "count": 0,
      "data": []
    }
  }
}
```