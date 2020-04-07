// index.jsx
import React from "react";
import ReactDOM from "react-dom";
import SubmitTextBox from './components/submitTextBox.jsx';

// TODO edit this
ReactDOM.render( <SubmitTextBox submitEndpoint="/API/schedule" /> , document.getElementById("content"));
