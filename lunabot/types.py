from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime


@dataclass_json
@dataclass
class Login:
    action: str = field(compare=False, hash=False, repr=True)


@dataclass_json
@dataclass
class User:
    id: str = field(compare=False, hash=False, repr=True)
    email: str = field(compare=False, hash=False, repr=True)
    token: str = field(compare=False, hash=False, repr=True)
    plan_id: str = field(compare=False, hash=False, repr=True,
                         metadata=config(field_name='planId'))
    plan_sub_status_: int = field(compare=False, hash=False, repr=True,
                                  metadata=config(field_name='planSubStatus'))
    plan_expired_at_: int = field(compare=False, hash=False, repr=True,
                                  metadata=config(field_name='planExpiredAt'))
    # prompts: list = field()
    created_at_: int = field(compare=False, hash=False, repr=True,
                             metadata=config(field_name='createdAt'))
    updated_at_: int = field(compare=False, hash=False, repr=True,
                             metadata=config(field_name='updatedAt'))

    @property
    def plan_sub_status(self):
        return datetime.fromtimestamp(self.plan_sub_status_)

    @property
    def plan_expired_at(self):
        return datetime.fromtimestamp(self.plan_expired_at_)

    @property
    def created_at(self):
        return datetime.fromtimestamp(self.created_at_)

    @property
    def updated_at(self):
        return datetime.fromtimestamp(self.updated_at_)
