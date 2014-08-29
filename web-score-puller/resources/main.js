var PitApp = angular.module('PitApp', []);
PitApp.controller('PitDisplayCtrl', function ($scope, $http, $timeout) {
  $scope.rankConfig = {widths: [0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.15, 0.1, 0.1]};
  $scope.resultConfig = {widths: [0.1, 0.1, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.13, 0.13], headerStyles:['','','danger','danger','danger','info','info','info','danger','info']};
  
  function updateData(){
    $http.get('data.json').success(function(data) {
      $scope.data = data;
      $timeout(function(){
        updateData();
      }, 10000);
    }).error(function() {
      console.log('error getting data');
      $timeout(function(){
        updateData();
      }, 10000);
    });
  }
  
  updateData();
  
  
  
})
.directive('datatable', function(scroll) {
  return {
    restrict : 'E',
    scope: {
      data:   '=data',
      config: '=config',
      title:  '@title'
    },
    templateUrl: 'resources/data-table-template.part.html',
    link: function (scope, element, attrs) {
      scroll($(element).find('.data-table-body-container'), 50);
    }
  };
})
.factory('scroll', function($timeout){
  function scroll(element, speed, callback){
    var viewportHeight = element.height();
    var contentHeight = element[0].scrollHeight;
    var scrollDistance = contentHeight-viewportHeight;
    
    element.animate({scrollTop:scrollDistance}, scrollDistance*speed, 'linear', function(){
      if(callback)
        callback();
      $timeout(function(){
        element.scrollTop(0);
        $timeout(function(){
          scroll(element, speed, callback);
        }, 1000);
      }, 1000);
    });
  }
  return scroll;
});