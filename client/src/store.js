import dispatcher from './dispatcher';
import {extendObservable, observable} from 'mobx';

class RecordStore {
    @observable index = null;
    @observable record = {};
}


const store = new RecordStore();

dispatcher.register((action) => {
    if (action.type == 'FETCH_RECORD') {
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
});

export default store;
