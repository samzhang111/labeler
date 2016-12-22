import React from 'react';
import DataAnnotator from './DataAnnotator';
import {shallow} from 'enzyme';

describe('DataAnnotator', ()=> {
    const makeDataAnnotator = (data, responses, callback) => {
        return (<DataAnnotator data={data} responses={responses} callback={callback}/>)
    };

    it('renders test data', () => {
        const testData = { docId: 123, title: 'doc1', content: 'hello world' }
        const testResponses = [{text: 'Yes', value: 1}, {text: 'No', value: 0}];
        const testCallback = jest.fn();
        let dataAnnotator = shallow(makeDataAnnotator(testData, testResponses, testCallback));

        dataAnnotator.find('[label="Yes"]').simulate('click');
        dataAnnotator.find('[data-submit-response]').simulate('click');

        expect(testCallback).toBeCalledWith(123, 1);
    });

});
