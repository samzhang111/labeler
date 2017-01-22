import dispatcher from './dispatcher';
import {extendObservable, observable} from 'mobx';

class Store {
    @observable index = null;
    @observable record = {};
    @observable labels = [];
    @observable completed = 0;
    @observable summary = [];

    submitLabel = (recordId, userId, labels) => {
        dispatcher.dispatch({
            type: 'LABEL_IN_PROGRESS'
        });
        fetch(`/api/data/${recordId}/label`, {
            method: "POST",
            body: JSON.stringify({labels, userId})
        }).then(response => {
            response.json().then(json => {
                if (json.index == recordId) {
                    dispatcher.dispatch({
                        type: 'LABEL_SUCCESS',
                        record: recordId
                    });
                } else {
                    dispatcher.dispatch({
                        type: 'LABEL_FAILURE',
                        message: json
                    });
                }
            });
        });
    }
}


const store = new Store();

dispatcher.register((action) => {
    if (action.type == 'FETCH_LABELS') {
        fetch('/api/labels').then((response) => {
            response.json().then((json) => {
                store.labels = json.labels;
            });
        });
    }
    if (action.type == 'FETCH_USER') {
        fetch(`/api/user/${action.user}`).then((response) => {
            response.json().then((json) => {
                store.completed = json.completed;
            });
        });
    }
    if (action.type == 'FETCH_RECORD' ||
             action.type == 'LABEL_SUCCESS') {
        store.index = null;
        store.record = {};

        fetch('/api/unlabeled').then((response) => {
            response.json().then((json) => {
                fetch(`/api/data/${json.index}`).then((dataResponse) => {
                    dataResponse.json().then((data) => {
                        store.index = json.index;
                        store.record = data;
                    });
                });
            });
        });
    }
    if (action.type == 'FETCH_SUMMARY') {
        fetch('/api/summary').then((response) => {
            response.json().then((json) => {
                store.summary = json;
            });
        });
    }
    if (action.type == 'LABEL_SUCCESS') {
        store.completed += 1;
    }
    if (action.type == 'LABEL_IN_PROGRESS') {
        store.index = -1;
        store.record = {};
    }
});

export default store;
