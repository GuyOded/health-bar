import React, { ChangeEvent } from 'react';
import './App.css';
import SimpleHealthbar from '../healthbars/SimpleHealthbar/SimpleHealthbar'
import '../../stylesheets-main/switch.css'
import '../../stylesheets-main/common.css'

type State = {
    isDark: boolean
}

class App extends React.Component<{}, State> {
    constructor(props: {}) {
        super(props)
        this.state = {isDark: true}
        this.setDarkMode()
    }

    handleChangeDarkMode = (event: ChangeEvent<HTMLInputElement>): void => {
        let isDark: boolean = event.target.checked

        this.setState({
            isDark: isDark
        }, this.setDarkMode)
    }

    render() {
        return (
            <div className="main-container">
                <div className="healthbar-container">
                    <h1 className="title">
                        HP
                    </h1>
                    <SimpleHealthbar></SimpleHealthbar>
                </div>
                <label id="darkModeSwitch" className="switch">
                    <input type="checkbox" defaultChecked={this.state.isDark} onChange={this.handleChangeDarkMode}></input>
                    <span className="slider round"></span>
                </label>
            </div>
        );
    }

    private setDarkMode(): void {
        let isDark: boolean = this.state.isDark

        if (isDark) {
            document.body.classList.add("dark")
        } else {
            document.body.classList.remove("dark")
        }
    }
}

export default App;
