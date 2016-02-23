import React from "react"
import { Link } from "react-router";

import NavLink from "./layout/navlink";

export default class Header extends React.Component {
	render() {
		return (
			<header>
				<ul>
					<NavLink to="/" text="Home"/>
					<NavLink to="/editor" text="Editor"/>
					<NavLink to="/user" text="User"/>
				</ul>
			</header>
		)
	}
}