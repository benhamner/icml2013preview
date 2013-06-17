var icml2013PreviewApp = angular.module('icml2013PreviewApp', ['ngResource'])
    .config(function($routeProvider) {
        $routeProvider.
            when('/', { controller: 'mainCtrl', templateUrl: 'main.html'}).
            otherwise({ redirectTo: '/' });
    })
    .factory('JsonService', function($resource) {
      return $resource('data.json');
    });

icml2013PreviewApp.controller('mainCtrl', function($scope, JsonService){
  JsonService.get(function(data){
    $scope.papers = data.papers;
    $scope.topics = data.topics;
    window.s = $scope;
  });

  $scope.sort_topic = function (topic) {
    $scope.papers.sort(function (p1, p2) {return p2.topics[topic]-p1.topics[topic]});
  }
});