pragma ComponentBehavior: Bound
import QtQuick.Layouts
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material
import "components"
import qmltypes.controllers 1.0
import QtCharts 2.6
import "plot.js" as PlotJS

RowLayout {
    id: grid
    signal cancelButtonPressed
    required property DriveController driveController

    Connections {
        target: grid.driveController
        function onVelocityValue(timestamp, velocity) {
            PlotJS.updatePlot(timestamp, velocity, xAxis);
        }
        function onDriveConnected() {
            PlotJS.initPlot(chart, xAxis, yAxis);
        }
        function onDriveDisconnected() {
            PlotJS.resetPlot(chart, xAxis);
        }
    }

    Keys.onUpPressed: event => {
        if (event.isAutoRepeat)
            return;
        upButton.state = "ACTIVE";
        grid.driveController.set_velocity(velocitySlider.value);
    }

    Keys.onDownPressed: event => {
        if (event.isAutoRepeat)
            return;
        downButton.state = "ACTIVE";
        grid.driveController.set_velocity(velocitySlider.value * -1);
    }

    Keys.onLeftPressed: event => {
        leftButton.state = "ACTIVE";
    }

    Keys.onRightPressed: event => {
        rightButton.state = "ACTIVE";
    }

    Keys.onReleased: event => {
        if (event.isAutoRepeat)
            return;
        switch (event.key) {
        case Qt.Key_Up:
            upButton.state = "NORMAL";
            break;
        case Qt.Key_Down:
            downButton.state = "NORMAL";
            break;
        case Qt.Key_Left:
            leftButton.state = "NORMAL";
            break;
        case Qt.Key_Right:
            rightButton.state = "NORMAL";
            break;
        }
        grid.driveController.set_velocity(0);
    }

    ColumnLayout {
        Layout.preferredWidth: 3

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: 2
            ChartView {
                id: chart
                anchors.fill: parent
                axes: [
                    ValueAxis {
                        id: xAxis
                        min: 1.0
                        max: 20.0
                    },
                    ValueAxis {
                        id: yAxis
                        min: -7.5
                        max: 7.5
                    }
                ]
            }
        }

        GridLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredWidth: 3
            Layout.preferredHeight: 1
            rows: 2
            columns: 4
            rowSpacing: 0
            SpacerH {
            }
            SpacerH {
            }
            SpacerH {
            }
            SpacerH {
            }
            SpacerW {
            }
            StateButton {
                id: upButton
                text: "↑"
                Layout.alignment: Qt.AlignBottom
            }
            SpacerW {
            }
            Dial {
                Layout.fillWidth: true
                Layout.rowSpan: 2
            }
            StateButton {
                id: leftButton
                text: "←"
                Layout.alignment: Qt.AlignRight
            }
            StateButton {
                id: downButton
                text: "↓"
                Layout.alignment: Qt.AlignTop
            }
            StateButton {
                id: rightButton
                text: "→"
                Layout.alignment: Qt.AlignLeft
            }
            SpacerH {
            }
            SpacerH {
            }
            SpacerH {
            }
            SpacerH {
            }
        }
    }

    ColumnLayout {
        id: rightColumn
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.preferredWidth: 1
        Text {
            Layout.fillWidth: true
            color: "black"
            text: "Velocity"
        }
        Slider {
            id: velocitySlider
            Layout.fillWidth: true
            from: 1
            to: 10
            value: 5
            onMoved: () => {
                yAxis.min = (velocitySlider.value * -1) - 2.5;
                yAxis.max = velocitySlider.value + 2.5;
            }
        }
        Text {
            Layout.fillWidth: true
            color: "black"
            text: "Speed"
        }
        Slider {
            Layout.fillWidth: true
            value: 0.5
        }
        Text {
            Layout.fillWidth: true
            color: "black"
            text: "Lorem"
        }
        Slider {
            Layout.fillWidth: true
            value: 0.5
        }
    }
}
