import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { subscribeToTimer } from './api'

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      connection_state: 'no connected yet',
      alert: ''
    };


    subscribeToTimer((err, connection_state, alert) => this.setState({
      connection_state,
      alert
    }));

  }

  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <p>
          This is the timer value: {this.state.connection_state}
        </p>
        <p>
          Alert: {this.state.alert}
        </p>
        <p></p>
      </div>
    );
  }
}

export default App;
