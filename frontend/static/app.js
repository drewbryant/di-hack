var app = angular.module("game-lobby", ["firebase"]);

app.controller("MainCtrl", MainCtrl);
function MainCtrl ($scope, $firebase, $http) {
  // TODO: wire in the firebase authn bits
  this.firebaseUrl = 'https://glaring-heat-2029.firebaseio.com';
  $scope.serverMaxUsers = 20; // minecraft constant

  this.serversRef = new Firebase(this.firebaseUrl + '/servers');
  this.allUsersRef = new Firebase(this.firebaseUrl + '/users');

  $scope.user = null;
  $scope.servers = $firebase(this.serversRef).$asObject();
  $scope.allUsers = $firebase(this.allUsersRef).$asObject();

  this.http = $http;
  this.scope = $scope;
  this.firebase = $firebase;

  // this.login('drew-id', 'the_real_ron_brn', 'Drew'); // FIXME: for debugging
}

MainCtrl.prototype.addFriend = function (minecraftUserId) {
  this.userRef
    .child('friends')
    .child(minecraftUserId)
    .set(true);
}

MainCtrl.prototype.getNumActiveUsers = function (server) {
  if (!server.active) {
    return 0;
  } else {
    return Object.keys(server.active).length;
  }
};

MainCtrl.prototype._getUserFirebasePath = function (userId) {
  return this.firebaseUrl + '/users/' + userId
}

MainCtrl.prototype.createNewUser = function (userId, minecraftUserId, displayName) {
  this.allUsersRef // FIXME: hack to auto-login during testing which clears all existing friends
    .child(userId)
    .set({
      minecraftUserId: minecraftUserId,
      online: true,
      displayName: displayName,
    });
  console.info('Created user: ', userId);
  this.login(userId);
}

MainCtrl.prototype.login = function (userId) {
  console.info('logging in the user: ', userId);
  // Create a sync'd object for the user, to drive the UI
  var userRefPath = this._getUserFirebasePath(userId);
  this.userRef = new Firebase(userRefPath);
  this.userRef.child('online').set(true);
  this.scope.user = this.firebase(this.userRef).$asObject();

  // Setup event handlers for friend adds/removes
  var friendsRef = new Firebase(userRefPath + '/friends');
  this.scope.friends = {};
  // Child added event will be called once for each value in the collection
  // (e.g., if there are already 3 friends, it will be invoked thrice immediately)
  friendsRef.on('child_added', this.handleFriendAdded.bind(this));
  friendsRef.on('child_removed', this.handleFriendRemoved.bind(this));
}

MainCtrl.prototype.logout = function (userId) {
  this.userRef.child('online').set(false);
  this.userRef = null;
  this.user = null;
}

MainCtrl.prototype._insertFriend = function (friendUserId) {
  // WARNING / FIXME: for the moment, assume that the arg is the real id
  // TODO: add another lookup map of minecraftId -> userId
  var friendRef = new Firebase(this._getUserFirebasePath(friendUserId));
  this.scope.friends[friendUserId] = this.firebase(friendRef).$asObject();
}

MainCtrl.prototype.handleFriendAdded = function (snapshot) {
  console.log('friend added: ', snapshot.key(), snapshot.val());
  this._insertFriend(snapshot.key());
}

MainCtrl.prototype.handleFriendRemoved = function (snapshot) {
  console.log('friend removed: ', snapshot.key(), snapshot.val());
  delete this.scope.friends[snapshot.key()];
}

MainCtrl.prototype.createServer = function (serverName, diskName) {
  console.info('creating an instance...', serverName, diskName);
  var uri = '/api/create?server=' + serverName + '&disk=' + diskName;

  // Create a record in Firebase that will be overwritten on successful creation of the VM
  this.serversRef
    .child(serverName)
    .child('ip')
    .child('external')
    .set(false);

  // TODO: move the content inline to avoid dealing with the modal
  $('#create-game-server-modal').hide();

  this.http.get(uri)
    .success(function(data, status, headers, config) {
      if (status === 200) {
        console.log('success!', arguments);
      } else {
        console.log('success, but non-200 response: ', status);
      }
    })
    .error(function(data, status, headers, config) {
      // TODO: add some error handling eventually
      console.log('error sending create instance request', arguments);
    });
};

var smoothSpinnerOptions = {
  lines: 15, // The number of lines to draw
  length: 3, // The length of each line
  width: 10, // The line thickness
  radius: 0, // The radius of the inner circle
  corners: 1, // Corner roundness (0..1)
  rotate: 0, // The rotation offset
  direction: 1, // 1: clockwise, -1: counterclockwise
  color: '#ccc', // #rgb or #rrggbb or array of colors
  speed: 1.2, // Rounds per second
  trail: 58, // Afterglow percentage
  className: 'spinner', // The CSS class to assign to the spinner
  top: '50%', // Top position relative to parent
  left: '88%' // Left position relative to parent
};

var blockSpinnerOptions = {
  lines: 11, // The number of lines to draw
  length: 4, // The length of each line
  width: 8, // The line thickness
  radius: 0, // The radius of the inner circle
  corners: 0, // Corner roundness (0..1)
  rotate: 0, // The rotation offset
  direction: 1, // 1: clockwise, -1: counterclockwise
  color: '#ccc', // #rgb or #rrggbb or array of colors
  speed: 1.5, // Rounds per second
  trail: 60, // Afterglow percentage
  shadow: false, // Whether to render a shadow
  hwaccel: true, // Whether to use hardware acceleration
  className: 'spinner', // The CSS class to assign to the spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  top: '50%', // Top position relative to parent
  left: '88%' // Left position relative to parent
};

app.directive('spinner', function() {
  return {
    restrict: 'E',
    template: '<span class="text-muted">Creating...</span>',
    replace: true,
    link: function(scope, element, attrs) {
      var spinner = new Spinner(blockSpinnerOptions).spin();
      element.append(spinner.el);
    }
  };
});
