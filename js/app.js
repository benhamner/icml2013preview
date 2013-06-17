var icml2013PreviewApp = angular.module('icml2013PreviewApp', ['ngResource'])
    .config(function($routeProvider) {
        $routeProvider.
            when('/', { controller: 'mainCtrl', templateUrl: 'main.html'}).
            otherwise({ redirectTo: '/' });
    })
    .factory('JsonService', function($resource) {
      return $resource('papers.json', {}, {get: {method:'GET', isArray: true} });
    });

icml2013PreviewApp.controller('mainCtrl', function($scope, JsonService){
  JsonService.get(function(data){
    $scope.papers = data;
    window.data = data;
  });
});