// index.jsx
import React from "react";
import ReactDOM from "react-dom";
import 'bootstrap/dist/css/bootstrap.css';
import SubmitTextBox from './components/submitTextBox.jsx';

// TODO edit this
ReactDOM.render( <SubmitTextBox submitEndpoint="/API/schedule" /> , document.getElementById("content"));
