import React from 'react';
import dispatcher from './dispatcher.js';
import {inject, observer} from 'mobx-react';
import './Summary.scss';

@inject('store') @observer
class Summary extends React.Component {
    componentDidMount() {
        dispatcher.dispatch({
            type: 'FETCH_SUMMARY'
        });
    };

    render() {
        const {store} = this.props;

        if (!store.summary.counts) {
            return <div>Loading...</div>
        }

        let i = 0;
        let label_count_rows = [];
        for (let row of store.summary.counts) {
            const label = row[0] === null ? 'Skipped' : row[0];
            const count = row[1];
            label_count_rows.push(<div key={i} className="summary-row"><span className="summary-cell">{label}</span> <span className="summary-cell">: {count}</span></div>);

            i += 1
        };

        let labelset_count_rows = [];
        for (let row of store.summary.labelset_counts) {
            const labelset = row[0] === null ? 'Skipped' : row[0];
            const count = row[1];
            labelset_count_rows.push(
            <div key={i} className="summary-row"><span className="summary-cell">{labelset}</span> <span className="summary-cell">: {count}</span></div>);

            i += 1
        };

        return <div className="summary-layout">
            <div className="total-count">Total Labels: {store.summary.total}</div>
            <div className="label-count-layout summary-table"> 
                <div className="summary-heading">Label counts (individual)</div>
                {label_count_rows} 
            </div>
            <div className="labelset-count-layout summary-table"> 
                <div className="summary-heading">Label counts (grouped)</div>
                {labelset_count_rows} </div>
        </div>
    }
}

export default Summary;
