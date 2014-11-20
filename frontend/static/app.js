var app = angular.module("game-lobby", ["firebase"]);
app.controller("MainCtrl", MainCtrl);

function MainCtrl ($scope, $firebase, $window) {
  // Assume we've done authn and know that we're presenting user Mary now
  // TODO: wire in the firebase authn bits
  var firebaseUrl = 'https://glaring-heat-2029.firebaseio.com';
  $scope.serverMaxUsers = 20; // minecraft constant

  var userId = "mary-id";

  var userRef = new Firebase(firebaseUrl + '/users/' + userId);
  var serverRef = new Firebase(firebaseUrl + '/servers');
  var allUsersRef = new Firebase(firebaseUrl + '/users');

  $scope.user = $firebase(userRef).$asObject();
  $scope.servers = $firebase(serverRef).$asObject();
  $scope.allUsers = $firebase(allUsersRef).$asObject();

}

MainCtrl.prototype.getNumActiveUsers = function (server) {
  if (!server.active) {
    return 0;
  } else {
    return Object.keys(server.active).length;
  }
}
