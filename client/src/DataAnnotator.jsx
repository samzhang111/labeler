import React from 'react';
import dispatcher from './dispatcher.js';
import {observer} from 'mobx-react';
import store from './store';

@observer
class DataAnnotator extends React.Component {
    componentDidMount() {
        dispatcher.dispatch({
            type: 'FETCH_RECORD'
        });
    };

    getDataRows(data) {
        let fields = [];
        for (let key of Object.keys(data)) {
            console.log('entry: ', key, data[key]);
            fields.push(
            <div key={key} className="data-row">
                <span className="key">{key}: </span>
                <span className="value">{data[key]}</span>
            </div>)
        }

        return fields;
    };

    render() {
        console.log('store: ', store);
        if (!store) {
            return <div>Loading...</div>
        }

        let dataTable = <div className="data-table">
            {this.getDataRows(store.record)}
        </div>

        return (<div>
            {dataTable}
        </div>)
    }
}

export default DataAnnotator;
