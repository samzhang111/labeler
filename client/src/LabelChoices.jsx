import React from 'react';
import "./LabelChoices.scss"

class LabelChoices extends React.Component {
    state = {
        selectedLabels: []
    };

    clickLabel = (e) => {
        if (e.target.checked) {
            this.setState({selectedLabels: [...this.state.selectedLabels, e.target.value]});
        } else {
            let ix = this.state.selectedLabels.indexOf(e.target.value);
            this.state.selectedLabels.splice(ix, 1);
        }
    }

    submit = (e) => {
        const {submitLabel, recordId} = this.props;
        submitLabel(recordId, this.state.selectedLabels)
    }

    render() {
        const {labels, recordId} = this.props;

        let options = [];
        for (let label of labels) {
            options.push(
            <div className="labels" key={label.value}>
                <label>
                    <input onChange={this.clickLabel} type="checkbox" value={label.value}/>
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
