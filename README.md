# 前端监控项目 Real User Monitoring

### 接口详情请翻阅文档

- app/
  - models.py 数据库模型
  - views/
    - action.py 用户行为数据查询接口
    - action.py 错误数据查询接口
    - http.py HTTP请求数据查询接口
    - manage.py 网站列表查询及信息修改接口
    - post.py 数据采集接口
    - timing.py 性能数据查询接口
    - urils.py 公用代码
- rum/
  - urls.py 路由配置