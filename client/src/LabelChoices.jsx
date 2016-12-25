import React from 'react';
import "./LabelChoices.scss"

class LabelChoices extends React.Component {
    state = {
        selectedLabel: -1
    };

    clickLabel = (e) => {
        this.setState({selectedLabel: e.target.value});
    }

    submit = (e) => {
        const {submitLabel, recordId} = this.props;
        submitLabel(recordId, this.state.selectedLabel)
    }

    render() {
        const {labels, recordId} = this.props;

        let options = [];
        for (let label of labels) {
            options.push(
            <div className="labels" key={label.value}>
                <label>
                    <input onClick={this.clickLabel} type="radio" value={label.value} name="labels"/>
                    {label.text}</label>
            </div>
            );
        }

        return (<form className="label-choices-layout">
            {options}
            <input className="submit-button" onClick={this.submit} type="button" value="Label"/>
        </form>)

    }
}

export default LabelChoices;
