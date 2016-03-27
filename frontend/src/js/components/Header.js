import React from "react"
import { Link } from "react-router";

import NavLink from "./layout/navlink";

export default class Header extends React.Component {
	render() {
		return (
			<header class="navbar navbar-inverse navbar-fixed-top">
                <div class="container">
                    <ul class="nav navbar-nav navbar-right">
                        <NavLink to="/" text="Home"/>
                        <NavLink to="/editor" text="Editor"/>
                        <NavLink to="/user" text="User"/>
                        <NavLink to="/login" text="Login"/>
                    </ul>
                </div>
			</header>
		)
	}
}
