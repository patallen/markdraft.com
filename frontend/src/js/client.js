import React from "react";
import ReactDOM from "react-dom";
import { Router, Route, hashHistory, IndexRoute } from "react-router";

import App from "./app";
import Editor from "./pages/Editor";
import Index from "./pages/Index";
import Login from "./pages/Login";
import User from "./pages/User";

import "../styles/main.scss"

ReactDOM.render((
	<Router history={hashHistory}>
		<Route path="/" component={App}>
			<IndexRoute component={Index}/>
			<Route path="/editor" component={Editor}/>
			<Route path="/user" component={User}/>
			<Route path="/login" component={Login}/>
		</Route>
	</Router>
), document.getElementById("app"))
