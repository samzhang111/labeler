import React from 'react';
import ReactDOM from 'react-dom';
import DataAnnotator from './DataAnnotator.jsx';
import store from './store';
import {Provider} from 'mobx-react';
import { Router, Route, hashHistory } from 'react-router'
 
class App extends React.Component {
  render() {
    return <div>
        <Provider store={store}>
            <Router history={hashHistory}>
                <Route path="/label/:userId" component={DataAnnotator} />
            </Router>
        </Provider>
    </div>
  }
}

ReactDOM.render(<App/>, document.getElementById('app'));
