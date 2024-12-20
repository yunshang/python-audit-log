import dataclasses
import functools
import json
import uuid
from collections.abc import Callable
from contextvars import ContextVar
from datetime import UTC, datetime
from functools import singledispatch
from typing import Any
from sqlalchemy.orm import Session

from audit_log.exceptions import AuditValidationError
from audit_log.schema import (
    SCHEMA_VERSION,
    ActionType,
    OutcomeResult,
    Principal,
)
from .models import AuditLog


@singledispatch
def to_serializable(val) -> dict | list | str:
    """Default serialization"""
    return str(val)


@to_serializable.register
def serialize_sets(val: set) -> list:
    """Convert sets to lists for serialization"""
    return list(val)


@to_serializable.register
def serialize_exceptions(val: Exception) -> str:
    """Convert exceptions to strings for serialization"""
    return repr(val)


json_dumps = functools.partial(json.dumps, default=to_serializable)

# Example use of ContextVar, TBD if this works well
REQ_ID: ContextVar[str | uuid.UUID] = ContextVar("request_id")


def log(
    action_type: ActionType,
    resource_type: str,
    resource_id: Any,
    result: OutcomeResult,
    principal: Principal,
    request_id: str | uuid.UUID | None = None,
    outcome_reason: str | None = None,
    before: Any | None = None,
    after: Any | None = None,
    serializer: Callable[[dict], str | bytes] = json_dumps,
    session: Session = None,
):
    now = datetime.now(tz=UTC).isoformat()
    request_id = request_id or REQ_ID.get()
    

    # 逻辑判断
    if result == OutcomeResult.SUCCEEDED:
        if resource_id is None:
            raise AuditValidationError("Missing resource ID")
        if action_type == ActionType.CREATE and after is None:
            raise AuditValidationError("Missing 'after' with CREATE action")
        if action_type == ActionType.UPDATE and (before is None or after is None):
            raise AuditValidationError(
                "Missing 'before' and 'after' with UPDATE action"
            )
        if action_type == ActionType.DELETE and before is None:
            raise AuditValidationError("Missing 'before' with DELETE action")

    # 创建审计日志条目
    audit_log_entry = AuditLog(
        action_type=action_type.value,
        resource_type=resource_type,
        resource_id=str(resource_id),
        result=result.value,
        principal_type=principal.type.value,
        principal_authority=principal.authority,
        principal_id=principal.id,
        request_id=str(request_id) if request_id else None,
        outcome_reason=outcome_reason,
        before=before,
        after=after,
    )
    
    # 将条目添加到会话并提交
    session.add(audit_log_entry)
    session.commit()
    
    # 继续打印日志
    print(
        serializer(
            {
                "type": "audit-log",
                "timestamp": now,
                "level": "INFO",
                "version": SCHEMA_VERSION,
                "resource": {"type": resource_type, "id": resource_id},
                "action": {"type": action_type},
                "outcome": {
                    "result": result,
                    "reason": outcome_reason,
                    "before": before,
                    "after": after,
                },
                "context": {"request": {"id": request_id}},
                "principal": dataclasses.asdict(principal),
            }
        )
    )
    
    # 关闭会话
    session.close()
