# Django Template

## Features

- 自定义授权用户
- JWT 认证
- 超级管理员、管理员、普通用户的权限控制

## Usage

1. 安装依赖

   ```bash
   pip install -r requirements.txt
   ```

2. 生成数据库迁移文件

   ```bash
   python manage.py makemigrations
   ```

3. 迁移数据库

   ```bash
    python manage.py migrate
    ```

4. 创建超级用户

   ```bash
   python manage.py createsuperuser
   ```

5. 运行项目

   ```bash
   python manage.py runserver
   ```
