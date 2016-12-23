import dispatcher from './dispatcher';
import {extendObservable, observable} from 'mobx';

class Store {
    @observable index = null;
    @observable record = {};
    @observable labels = [];
    submitLabel = (recordId, labels) => {
        dispatcher.dispatch({
            type: 'LABEL_IN_PROGRESS'
        });
        fetch(`/data/${recordId}/label`, {
            method: "POST",
            body: JSON.stringify({labels})
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
        fetch('/labels').then((response) => {
            response.json().then((json) => {
                store.labels = json.labels;
            });
        });
    }
    else if (action.type == 'FETCH_RECORD' ||
             action.type == 'LABEL_SUCCESS') {
        fetch('/unlabeled').then((response) => {
            response.json().then((json) => {
                fetch(`/data/${json.index}`).then((dataResponse) => {
                    dataResponse.json().then((data) => {
                        store.index = json.index;
                        store.record = data;
                    });
                });
            });
        });
    }
    else if (action.type == 'LABEL_IN_PROGRESS') {
        store.index = -1;
        store.record = {};
    }
});

export default store;
