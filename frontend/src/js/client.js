import React from "react";
import ReactDOM from "react-dom";
import { Router, Route, hashHistory, IndexRoute } from "react-router";

import App from "./app";
import Editor from "./pages/editor";
import Index from "./pages/index";
import User from "./pages/user";

import "../styles/main.scss"

ReactDOM.render((
	<Router history={hashHistory}>
		<Route path="/" component={App}>
			<IndexRoute component={Index}/>
			<Route path="/editor" component={Editor}/>
			<Route path="/user" component={User}/>
		</Route>
	</Router>
), document.getElementById("app"))
