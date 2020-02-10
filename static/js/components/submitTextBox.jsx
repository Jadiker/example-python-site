import React from 'react';
import {jsonify} from "../util.js"

// there are two phases:
// 1: Query for an ID (ID)
// 2: Poll for information about that ID (POLL)
// For (1) we need to know the key to send the info needed to get an ID
// ...and what key the ID is coming back in
const SINGLE_VALUE_KEY = 'key';

export default class SubmitTextBox extends React.Component {
    // polling code from https://stackoverflow.com/a/51972967/
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = {
            response: null
        }
        /*
        this.props = {
            submitEndpoint,

            textId,
            textLabel,
            boxName,
            buttonLabel
        }
        */
    }

    handleSubmit(event) {
        event.preventDefault(); // don't have the browser refresh on submit
        const data = new FormData(event.target);

        var json = jsonify(data);

        // console.log("JSONized");
        // console.log(json);
        //
        // console.log("sending the data to:");
        // console.log(this.props.submitEndpoint);

        var response;

        fetch(this.props.submitEndpoint, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: json,
            })
        .then(jsonResponse => jsonResponse.json())
        .then(responsePromise => response = responsePromise)
        // you must continue to use `.then`; otherwise, response is undefined
        // .then(() => console.dir(response))
        .then(() => this.setState({response: response[SINGLE_VALUE_KEY]}));
    }

    // the name of the input determines its key in the JSON
    render() {
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <label htmlFor={this.props.id}>{this.props.textLabel}</label>
                    <textarea class="form-control" id={this.props.inputId} name={this.props.boxName} rows="6" />
                    <button>{this.props.buttonLabel}</button>
                </form>
                <p>{this.props.responseLabel}</p>
                <pre>{this.state.response || "No Response"}</pre>
            </div>
        );
    }
}

SubmitTextBox.defaultProps = {
    inputId: "statements",
    textId: "submitTextBox",
    textLabel: "Write out your schedule: ",
    responseLabel: "The response from the server:",
    boxName: SINGLE_VALUE_KEY, // should be the key used to send the data to the server
    buttonLabel: "Send input!"
}
