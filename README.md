# Audit Log Library

## 简介

这是一个用于审计日志记录的 Python 库，支持通过 Alembic 进行数据库迁移。该库提供了从请求头中提取用户身份的功能，并支持记录各种操作的审计日志。

### 创建 `.env` 文件

在项目根目录下创建一个 `.env` 文件，并添加您的数据库连接字符串：

```
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/audit_logs?charset=utf8
```

请根据您的数据库配置替换 `username` 和 `password`。

## 使用方法

### 初始化

在您的 Python 项目中，您可以通过以下方式导入库：

```python
from audit_log import  run_specific_migration
```

### 设置审计日志表

要创建审计日志表并运行迁移，请调用 `setup_audit_logs` 方法：

```python
 run_specific_migration()
```

### 运行特定迁移

如果您需要运行特定的迁移，可以使用 `run_specific_migration` 方法，传入修订 ID：

### 记录审计日志

您可以在您的应用程序中使用 `AuditLog` 模型来记录审计日志。以下是一个示例：

```python
from audit_log.models import AuditLog
from sqlalchemy.orm import sessionmaker
创建数据库会话
Session = sessionmaker(bind=engine)
session = Session()
创建审计日志条目
audit_log_entry = AuditLog(
action_type="CREATE",
resource_type="User",
resource_id="123",
result="SUCCEEDED",
principal_type="USER",
principal_authority="example.com",
principal_id="user@example.com",
request_id="req-456",
outcome_reason="Created successfully",
before=None,
after="{'name': 'John Doe'}"
)
将条目添加到会话并提交
session.add(audit_log_entry)
session.commit()
session.close()
```

### 解析请求头

您可以从请求头中提取用户身份信息，使用 `get_principal_from_headers` 方法：

```python
from audit_log.headers import get_principal_from_headers
headers = {
"x-jwt-claim-iss": "example.com",
"x-jwt-claim-sub": "user@example.com",
"x-jwt-claim-sub-type": "USER"
}
principal = get_principal_from_headers(headers)
print(principal)
```

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。

## 许可证

该项目使用 MIT 许可证。有关详细信息，请参阅 LICENSE 文件。
