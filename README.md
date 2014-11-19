di-hack
=======


### Firebase data schema:

* Alice is in-game on server foo
* Bob is offline
* Mary is online, in lobby

```
{

  "users": {
    "alice-id": {
      "displayName": "Alice",
      "minecraftUserId": "block_builder_123",
      "server": "foo",
      "online": true,
      "friends": {
        "mary-id": true
      }
    },
    "bob-id": {
      "displayName": "Bob",
      "minecraftUserId": "make_some_fire",
      "server": null,
      "online": false,
      "friends": {}
    },
    "mary-id": {
      "displayName": "Mary",
      "minecraftUserId": "more_blocks_pls",
      "server": null,
      "online": true,
      "friends": {
        "alice-id": true
      }
    }
  },

  "servers": {
    "foo": {
      "ipAddress": "123.45.67.89",
      "active": {
        "alice-id": true
      }
    }
  },

  "lobby": {
    "users": {
      "mary-id": true
    }
  }

}
```

