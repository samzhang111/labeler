import React from 'react';
import {shallow} from 'enzyme';
import LabelChoices from './LabelChoices.jsx';

describe('LabelChoices', () => {
    it('sends the document ID, the user ID, and all of the checked boxes as a list on submit', () => {
        const submitLabel = jest.fn();
        const testLabels = [{value: 0, text: 'hi'}, {value: 1, text: 'bye'}, {value: 3, text: 'not chosen'}];
        const testUserId = 'test-id';
        const testDocumentId = 12345;
        let labelChoices = shallow(<LabelChoices labels={testLabels} recordId={testDocumentId} submitLabel={submitLabel} userId={testUserId}/>);

        labelChoices.find('input[value=0]').simulate('change', {target: {checked: true, value: 0}});
        labelChoices.find('input[value=1]').simulate('change', {target: {checked: true, value: 1}});

        labelChoices.find('.submit-button').simulate('click');

        expect(submitLabel).toBeCalledWith(testDocumentId, testUserId, [0, 1]);
    });
});
