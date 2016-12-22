import React from 'react';
import ReactDOM from 'react-dom';
import DataAnnotator from './DataAnnotator.jsx';
import store from './store';
import {Provider} from 'mobx-react';
 
class App extends React.Component {
  render() {
    return <div>
        <Provider store={store}>
            <DataAnnotator />
        </Provider>
    </div>
  }
}

ReactDOM.render(<App/>, document.getElementById('app'));
