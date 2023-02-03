# expert_core

- [Permissions](#permissions)
  - [1. Init](#1-init)
  - [2. Get current user](#2-get-current-user)
  - [3. Set user permission](#3-set-user-permissions)
  - [4. Check user permission](#4-check-user-permissions)
  - [5. Uset user permissions](#5-unset-user-permissions)
  - [6. Set inherit user permissions](#6-set-inherit-user-permissions)
  - [7. Check inherit user permissions](#7-check-inherit-user-permissions)
- [Migrations](#migrations)
  - [1. Generate migration](#1-generate-migration)
  - [2. Migrate](#2-migrate)
  - [3. Downgrade](#3-downgrade)

## Requirements

- python 3.10+

```bash
pip install pip install git+ssh://git@github.com/expertspec/expert_core.git@{tag}
```

## Permissions 

### 1. Init

```python
from fastapi import FastAPI

from expert_core.plugins import init_keycloak


app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_keycloak(app)
```

### 2. Get current user

```python
from fastapi import Depends

from expert_core.plugins.keycloak import depends_authentication, OIDCUser


@app.get("/user")
async def get_user(user: OIDCUser = Depends(depends_authentication())):
    user_id = user.sub
```


### 3. Set user permissions

```python
from fastapi import Depends, Path
from pydantic.types import UUID4

from expert_core.plugins.keycloak import depends_authentication, depends_idp, Keycloak, OIDCUser


@app.post("/chat/{item_id}/set")
async def set_user_permissions(
    chat_id: UUID4 = Path(..., alias="item_id"),
    user: OIDCUser = Depends(depends_authentication()),
    idp: Keycloak = Depends(depends_idp)
):
    _chat_id = str(chat_id)

    await idp.update_permissions(user, chat_id, permissions="rw------")
```

### 4. Check user permissions

```python
from fastapi import Depends, Path
from pydantic.types import UUID4

from expert_core.plugins.keycloak import depends_permissions, OIDCUser


@app.get("/chat/{chat_id}/get")
async def check_user_permissions(
    chat_id: UUID4,
    user: OIDCUser = Depends(depends_permissions("rw.*", param="chat_id", in_="path")),
):
    pass
```

### 5. Unset user permissions

```python
from fastapi import Depends, Path
from pydantic.types import UUID4

from expert_core.plugins.keycloak import depends_authentication, depends_idp, Keycloak, OIDCUser


@app.delete("/chat/{item_id}/unset")
async def unset_user_permissions(
    chat_id: UUID4 = Path(..., alias="item_id"),
    user: OIDCUser = Depends(depends_authentication()),
    idp: Keycloak = Depends(depends_idp)
):
    _chat_id = str(chat_id)

    await idp.update_permissions(user, chat_id)
    # or
    await idp.update_permissions(user, chat_id, permissions=None)
    # or
    await idp.update_permissions(user, chat_id, permissions="")
```


### 6. Set inherit user permissions

```python
from fastapi import Depends, Path
from pydantic.types import UUID4

from expert_core.plugins.keycloak import depends_authentication, depends_idp, Keycloak, OIDCUser


@app.post("/chat/{chat_id}/message/{message_id}/set")
async def set_inherit_user_permissions(
    chat_id: UUID4,
    message_id: UUID4,
    user: OIDCUser = Depends(depends_authentication()),
    idp: Keycloak = Depends(depends_idp)
):
    _chat_id = str(chat_id)
    _message_id = str(message_id)

    await idp.update_permissions(user, chat_id, _message_id, permissions="rwx-----")
```


### 7. Check inherit user permissions

```python
from fastapi import Depends, Path
from pydantic.types import UUID4

from expert_core.plugins.keycloak import depends_permissions, OIDCUser


@app.get("/chat/{chat_id}/message/{message_id}/get")
async def check_inherit_user_permissions(
    chat_id: UUID4,
    message_id: UUID4,
    user: OIDCUser = Depends(
        depends_permissions(
            "r.*",
            param=["chat_id", "message_id"],
            in_="path",
        ),
    ),
    ''' or 
    user: OIDCUser = Depends(
        depends_permissions(
            "r.*",
            param=["chat_id", "message_id"],
            in_=["path", "path"],
        ),
    ),
    '''
):
    pass
```

other examples:
```python
depends_permissions("rw.*", param="chat_id", in_="body")
depends_permissions("rw.*", param=["chat_id", "message_id"], in_="body")
depends_permissions("rw.*", param=["chat_id", "message_id"], in_=["body", "path"])
depends_permissions("rw.*", param=["chat_id", "message_id", "user_id"], in_=["path", "query", "body"])
```