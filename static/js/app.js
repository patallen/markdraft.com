var app = angular.module('drawerApp', ['ngResource']);
app.factory("Doc", function($resource){
	return $resource("/api/docs/:id");
});
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});
app.controller('DrawerController', function($scope, Doc){
	Doc.query(function(data){
		$scope.documents = data;
		console.log($scope.documents);
	});
});
