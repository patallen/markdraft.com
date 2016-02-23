import React from "react";
import Footer from "./components/footer";
import Header from "./components/header";


export default class App extends React.Component{
	render () {
		return (
			<div>
				<Header/>
				{this.props.children}
			</div>
		)
	}
}