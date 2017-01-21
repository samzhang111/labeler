import React from 'react';
import dispatcher from './dispatcher.js';
import {inject, observer} from 'mobx-react';
import LabelChoices from './LabelChoices.jsx';
import './DataAnnotator.scss';

const UserSummary = ({userId, completed}) => (
        <div className="user-summary-layout">
            <div>You: {userId}</div>
            <div># Completed: {completed}</div>
        </div>);

@inject('store') @observer
class DataAnnotator extends React.Component {
    componentDidMount() {
        dispatcher.dispatch({
            type: 'FETCH_LABELS'
        });
        dispatcher.dispatch({
            type: 'FETCH_RECORD'
        });
        dispatcher.dispatch({
            type: 'FETCH_USER',
            user: this.props.params.userId
        });
    };

    getUserId = (query) => {
        return query.workerId || 'none';
    }

    componentWillReceiveProps = (nextProps) => {
        const newUserId = this.getUserId(nextProps.location.query);
        const oldUserId = this.getUserId(this.props.location.query);
        console.log(newUserId, oldUserId);
        if (newUserId != oldUserId) {
            dispatcher.dispatch({
                type: 'FETCH_USER',
                user: newUserId
            });
        }
    }

    getDataRows(data) {
        let fields = [];
        for (let key of Object.keys(data)) {
            fields.push(
            <div key={key} className="data-row">
                <span className="key">{key}: </span>
                <span className="value"><pre>{data[key]}</pre></span>
            </div>)
        }

        return fields;
    };

    render() {
        const {store, location} = this.props;
        if (!store || store.index == -1 || !store.labels) {
            return <div>Loading...</div>
        }

        const userId = this.getUserId(location.query);

        let dataTable = <div className="data-table">
            {this.getDataRows(store.record)}
        </div>

        return (<div className="annotator-layout">
            <div className="annotator-row">
                <div className="annotator-left">
                    <UserSummary userId={userId} completed={store.completed} />
                    <p />
                    <LabelChoices
                        userId={userId}
                        labels={store.labels}
                        recordId={store.index}
                        submitLabel={store.submitLabel}
                    />
                </div>
                <div className="annotator-right">
                    <h1>ID: {store.index}</h1>
                    {dataTable}
                </div>
            </div>
        </div>)
    }
}

export default DataAnnotator;
