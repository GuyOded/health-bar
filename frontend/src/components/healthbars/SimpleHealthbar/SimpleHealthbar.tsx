import React, { Component } from 'react';
import "./SimpleHealthbar.css"

type HealthbarState = {
    hp: number
}

export class SimpleHealthbar extends Component<{}, HealthbarState> {
    private readonly healthBarWrapper: React.RefObject<HTMLDivElement>
    private static readonly MAX_HP = 100

    constructor(props: {}) {
        super(props)
        this.state = { hp: SimpleHealthbar.MAX_HP }
        this.healthBarWrapper = React.createRef()
    }

    render() {
        return (
            <div ref={this.healthBarWrapper} className="healthbar-wrapper"
                onMouseDown={this.onMouseDown}
                onMouseUp={this.onMouseUp}
                onMouseLeave={this.onMouseLeave}
                onTouchMove={this.onTouchMove}>
                <div className="healthbar" style={{ width: this.state.hp + "%" }}>
                </div>
            </div>
        );
    }

    //#region EventHandlers
    private onMouseDown = (event: React.MouseEvent): void => {
        const healthPoints: number = this.calculateHealthBasedOnMousePosition(event.pageX)
        this.setState({ hp: healthPoints }, () => {
            this.healthBarWrapper.current?.addEventListener('mousemove', this.onMouseMove)
        })
    }

    private onMouseMove = (event: MouseEvent) => {
        const healthPoints: number = this.calculateHealthBasedOnMousePosition(event.pageX)
        this.setState({ hp: healthPoints })
    }

    private onTouchMove = (event: React.TouchEvent) => {
        const healthPoints: number = this.calculateHealthBasedOnMousePosition(event.changedTouches[0].pageX)
        this.setState({ hp: healthPoints })
    }

    private onMouseUp = (event: React.MouseEvent) => {
        this.healthBarWrapper.current?.removeEventListener('mousemove', this.onMouseMove)

        const healthPoints: number = this.calculateHealthBasedOnMousePosition(event.pageX)
        this.setState({ hp: healthPoints })
    }

    private onMouseLeave = (event: React.MouseEvent) => {
        this.healthBarWrapper.current?.removeEventListener('mousemove', this.onMouseMove)
    }
    //#endregion EventHandlers

    private calculateHealthBasedOnMousePosition = (eventXPosition: number): number => {
        let relativeXPosition: number = eventXPosition - (this.healthBarWrapper.current?.offsetLeft as number)

        if (relativeXPosition < 0) {
            relativeXPosition = 0
        } else if (relativeXPosition > (this.healthBarWrapper.current?.clientWidth as number)) {
            relativeXPosition = (this.healthBarWrapper.current?.clientWidth as number)
        }

        // convert from clientWidth to a percentile scale
        let healthPoints = (relativeXPosition / (this.healthBarWrapper.current?.clientWidth as number)) * SimpleHealthbar.MAX_HP
        healthPoints = Math.round(healthPoints)

        return healthPoints
    }
}

export default SimpleHealthbar