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
