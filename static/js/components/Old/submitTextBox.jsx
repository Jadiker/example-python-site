import React from 'react';
import {jsonify} from "../util.js"

export default class SubmitTextBox extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();
        const data = new FormData(event.target);

        var json = jsonify(data);

        console.log("JSONized");
        console.log(json);

        console.log("sending the data to:");
        console.log(this.props.submitEndpoint);

        fetch(this.props.submitEndpoint, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: json,
            })
            .then((response) => response.json().then((data) => console.dir(data)));
    }


    // the name of the input determines its key in the JSON
    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label htmlFor={this.props.id}>{this.props.textLabel}</label>
                <input id={this.props.id} name={this.props.boxName} type="text" />
                <button>{this.props.buttonLabel}</button>
            </form>
        );
    }
}

SubmitTextBox.defaultProps = {
    id: "submitTextBox",
    textLabel: "Text:",
    boxName: "text",
    buttonLabel: "Send data!"
}
