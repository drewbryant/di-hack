var app = angular.module("game-lobby", ["firebase"]);

app.controller("MainCtrl", MainCtrl);
function MainCtrl ($scope, $firebase, $http) {
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

  this.http = $http;

}

MainCtrl.prototype.getNumActiveUsers = function (server) {
  if (!server.active) {
    return 0;
  } else {
    return Object.keys(server.active).length;
  }
}

MainCtrl.prototype.createServer = function (serverName, diskName) {
  console.info('creating an instance...', serverName, diskName);
  var uri = '/api/create?server=' + serverName + '&disk=' + diskName;
  console.log('create uri: ', uri);
  this.http.get(uri)
    .success(function(data, status, headers, config) {
      console.log('success!', arguments);
      if (status === 200) {
        // TODO: should make a modal directive that manipulates the dismiss property of the component
        $('#create-game-server-modal').hide();
      }
    })
    .error(function(data, status, headers, config) {
      console.log('error sending create instance request', arguments);
    });
}
