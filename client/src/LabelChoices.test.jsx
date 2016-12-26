import React from 'react';
import {shallow} from 'enzyme';
import LabelChoices from './LabelChoices.jsx';

describe('LabelChoices', () => {
    it('sends all of the checked boxes as a list on submit', () => {
        const submitLabel = jest.fn();
        const testLabels = [{value: 0, text: 'hi'}, {value: 1, text: 'bye'}, {value: 3, text: 'not chosen'}];
        const testId = 12345;
        let labelChoices = shallow(<LabelChoices labels={testLabels} recordId={testId} submitLabel={submitLabel}/>);

        labelChoices.find('input[value=0]').simulate('change', {target: {checked: true, value: 0}});
        labelChoices.find('input[value=1]').simulate('change', {target: {checked: true, value: 1}});

        labelChoices.find('.submit-button').simulate('click');

        expect(submitLabel).toBeCalledWith(testId, [0, 1]);
    });
});
