import React from 'react';
import dispatcher from './dispatcher.js';
import {inject, observer} from 'mobx-react';
import LabelChoices from './LabelChoices.jsx';
import './DataAnnotator.scss';

@inject('store') @observer
class DataAnnotator extends React.Component {
    componentDidMount() {
        dispatcher.dispatch({
            type: 'FETCH_LABELS'
        });
        dispatcher.dispatch({
            type: 'FETCH_RECORD'
        });
    };

    getDataRows(data) {
        let fields = [];
        for (let key of Object.keys(data)) {
            fields.push(
            <div key={key} className="data-row">
                <span className="key">{key}: </span>
                <span className="value">{data[key]}</span>
            </div>)
        }

        return fields;
    };

    render() {
        const {store} = this.props;
        if (!store || store.index == -1 || !store.labels) {
            return <div>Loading...</div>
        }

        let dataTable = <div className="data-table">
            {this.getDataRows(store.record)}
        </div>

        return (<div className="annotator-layout">
            <h1>ID: {store.index}</h1>
            {dataTable}
            <LabelChoices
                labels={store.labels}
                recordId={store.index}
                submitLabel={store.submitLabel}
            />
        </div>)
    }
}

export default DataAnnotator;
