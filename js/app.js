var icml2013PreviewApp = angular.module('icml2013PreviewApp', ['ngResource', 'infinite-scroll', 'ui.bootstrap'])
    .config(function($routeProvider) {
        $routeProvider.
            when('/', { controller: 'mainCtrl', templateUrl: 'views/main.html'}).
            otherwise({ redirectTo: '/' });
    })
    .factory('JsonService', function($resource) {
      return $resource('data/data.json');
    });

icml2013PreviewApp.controller('mainCtrl', function($scope, JsonService){
  $scope.papers = [];

  JsonService.get(function(data){
    $scope.papers = data.papers;
    $scope.topics = data.topics;
    topicSelection = _.map($scope.topics, function(topic) {return false;});
    topicSelection[0] = true;
    $scope.resort_papers_by_topic(topicSelection);
    window.s = $scope;
  });

  $scope.switch_topic = function (topic) {
    $scope.topicSelection[topic] = !$scope.topicSelection[topic];
    $scope.resort_papers_by_topic($scope.topicSelection);
  }

  $scope.sortByWord = function (word) {
    $scope.resetSelection();
    $scope.papers.sort(function (p1, p2) {
      i1 = p1.most_common.indexOf(word)
      i2 = p2.most_common.indexOf(word)
      if (i1<0) {i1 = 100000;}
      if (i2<0) {i2 = 100000;}
      return i1-i2;
    });
    $scope.sortedWord = word;
    $scope.refreshPapersTruncated();
  }

  $scope.sortByAuthor = function (author) {
    $scope.resetSelection();
    $scope.papers.sort(function (p1, p2) {
      i1 = p1.authors.indexOf(author)
      i2 = p2.authors.indexOf(author)
      if (i1<0) {i1 = 10000;}
      if (i2<0) {i2 = 10000;}
      return i1-i2;
    });
    $scope.sortedAuthor = author;
    $scope.refreshPapersTruncated();
  }

  $scope.resort_papers_by_topic = function (topicSelection) {
    $scope.resetSelection();
    $scope.topicSelection = topicSelection
    $scope.papers.sort(function (p1, p2) {
      return _.reduce(_.map(_.range($scope.topics.length), function (topic) {
        if ($scope.topicSelection[topic]) {
          return p2.topics[topic]-p1.topics[topic];
        }
        return 0;
      }), function (a1, a2) {return a1+a2;}, 0);});
    $scope.refreshPapersTruncated();
  }

  $scope.resetSelection = function() {
    $scope.sortedAuthor = "";
    $scope.sortedWord = "";
    $scope.topicSelection = _.map($scope.topics, function(topic) {return false;});
  }

  $scope.refreshPapersTruncated = function() {
    $scope.papersTruncated = $scope.papers.slice(0, 10);
    scroll(0,0);
  }

  $scope.papersTruncated = [];

  $scope.addMorePapers = function() {
    var n = $scope.papersTruncated.length;
    $scope.papers.slice(n, n+10).forEach(function(p) {$scope.papersTruncated.push(p);});
  }

  $scope.tipsOpen = function () {
    $scope.shouldBeOpen = true;
  };

  $scope.tipsClose = function () {
    $scope.closeMsg = 'I was closed at: ' + new Date();
    $scope.shouldBeOpen = false;
  };

  $scope.tipsOpts = {
    backdropFade: true,
    dialogFade:true
  };

});