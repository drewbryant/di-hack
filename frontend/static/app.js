var app = angular.module("game-lobby", ["firebase"]);
app.controller("MainCtrl", function($scope, $firebase) {
  // Assume we've done authn and know that we're presenting user Mary now
  // TODO: wire in the firebase authn bits
  var userId = "mary-id";
  var userFirebase = new Firebase("https://glaring-heat-2029.firebaseio.com/users/" + userId);
  var serverFirebase = new Firebase("https://glaring-heat-2029.firebaseio.com/servers");
  var lobbyFirebase = new Firebase("https://glaring-heat-2029.firebaseio.com/lobby");

  $scope.user = $firebase(userFirebase).$asObject();

  $scope.servers = $firebase(serverFirebase).$asObject();

  $scope.serverMaxUsers = 20; // minecraft constant

  // $scope.addFriend = function(name) {
  //   $scope.friends.$add({text: name});
  // }
  // $scope.addFriend('Alice'); $scope.addFriend('London');
});

/*

Firebase data schema:
* Alice is in-game on server foo
* Bob is offline
* Mary is online, in lobby
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
      "users": {
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

User ids:
* Using the built-in authentication mechanisms (google oauth) that also generate user ids

Server ids:
* names selected at creation time

*/
