import React from 'react';

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
                <label>{label.text}</label>
                <input onClick={this.clickLabel} type="radio" value={label.value} name="labels"/>
            </div>
            );
        }

        return (<form>
            {options}
            <input onClick={this.submit} type="button" value="Label"/>
        </form>)

    }
}

export default LabelChoices;
