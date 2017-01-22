import React from 'react';
import dispatcher from './dispatcher.js';
import {inject, observer} from 'mobx-react';
import './Summary.scss';

const countTable = (data, nullMessage='Skipped') => {
        let i = 0;
        let rows = [];
        for (let row of data) {
            const label = row[0] === null ? nullMessage : row[0];
            const count = row[1];
            rows.push(
            <div key={i} className="summary-row">
                <span className="summary-cell">{label}</span>
                <span className="summary-cell">: {count}</span>
            </div>);

            i += 1
        };

        return rows;
}

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

        let labelset_count_rows = countTable(store.summary.labelset_counts);
        let count_rows = countTable(store.summary.counts);
        let user_count_rows = countTable(store.summary.user_counts, 'None');

        return <div className="summary-layout">
            <div className="total-count">Total Labels: {store.summary.total}</div>
            <div className="total-count">Total Documents: {store.summary.total_docs}</div>
            <div className="label-count-layout summary-table"> 
                <div className="summary-heading">Label counts (individual)</div>
                {count_rows} 
            </div>
            <div className="labelset-count-layout summary-table"> 
                <div className="summary-heading">Label counts (grouped)</div>
                {labelset_count_rows} 
            </div>
            <div className="user-count-layout summary-table"> 
                <div className="summary-heading">User activity</div>
                {user_count_rows} 
            </div>
        </div>
    }
}

export default Summary;
