# 武汉大学研究生课程助手 

该程序适用于武汉大学研究生管理系统，主要作用为解析课表并发送邮件

## 依赖
python3  
BeautifulSoup4  
requests  

## 说明
config.py 配置文件  
accouts.py 身份证  
login.py 登录研究生系统并获取cookie  
course.py 定义课表类  
getTimeTable.py 获取课表并将课表解析为course对象  
mail.py  发送邮件

stopWater.py 停水通知
