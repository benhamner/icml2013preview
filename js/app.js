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
    $scope.topicSelection = _.map($scope.topics, function(topic) {return false;});
    $scope.topicSelection[0] = true;
    $scope.sortedByWord = false
    $scope.sortedWord = "";
    window.s = $scope;
  });

  $scope.switch_topic = function (topic) {
    $scope.topicSelection[topic] = !$scope.topicSelection[topic];
    $scope.resort_papers_by_topic();
  }

  $scope.sortByWord = function (word) {
    $scope.topicSelection = _.map($scope.topics, function(topic) {return false;});
    $scope.papers.sort(function (p1, p2) {
      i1 = p1.most_common.indexOf(word)
      i2 = p2.most_common.indexOf(word)
      if (i1<0) {i1 = p1.most_common.length;}
      if (i2<0) {i2 = p2.most_common.length;}
      return i1-i2;
    });
    $scope.sortedWord = word;
  }

  $scope.resort_papers_by_topic = function () {
    $scope.sortedWord = "";
    $scope.papers.sort(function (p1, p2) {
      return _.reduce(_.map(_.range($scope.topics.length), function (topic) {
        if ($scope.topicSelection[topic]) {
          return p2.topics[topic]-p1.topics[topic];
        }
        return 0;
      }), function (a1, a2) {return a1+a2;}, 0);});
  }

});