import React, { Component } from 'react';
import "./SimpleHealthbar.css"

type HealthbarState = {
    hp: number
}

export class SimpleHealthbar extends Component<{}, HealthbarState> {
    render() {
        return <div className="healthbar"></div>
    }
}

export default SimpleHealthbar