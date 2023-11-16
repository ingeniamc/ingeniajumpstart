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
        function onVelocityLeft(timestamp, velocity) {
            PlotJS.updatePlot(chartL, timestamp, velocity);
        }
        function onVelocityRight(timestamp, velocity) {
            PlotJS.updatePlot(chartR, timestamp, velocity);
        }
        function onDriveConnected() {
            PlotJS.initSeries(chartL, xAxisL, yAxisL, "Left");
            PlotJS.initSeries(chartR, xAxisR, yAxisR, "Right");
        }
        function onDriveDisconnected() {
            PlotJS.resetPlot(chartL);
            PlotJS.resetPlot(chartR);
        }
    }

    Keys.onUpPressed: event => {
        if (event.isAutoRepeat)
            return;
        upButton.state = "ACTIVE";
        if (leftCheck.checked) {
            grid.driveController.set_velocity(velocitySliderL.value, "LEFT");
        }
        if (rightCheck.checked) {
            grid.driveController.set_velocity(velocitySliderR.value, "RIGHT");
        }
    }

    Keys.onDownPressed: event => {
        if (event.isAutoRepeat)
            return;
        downButton.state = "ACTIVE";
        if (leftCheck.checked) {
            grid.driveController.set_velocity(velocitySliderL.value * -1, "LEFT");
        }
        if (rightCheck.checked) {
            grid.driveController.set_velocity(velocitySliderR.value * -1, "RIGHT");
        }
    }

    Keys.onLeftPressed: event => {
        if (event.isAutoRepeat || !rightCheck.checked || !leftCheck.checked)
            return;
        leftButton.state = "ACTIVE";
        grid.driveController.set_velocity(velocitySliderL.value * -1, "LEFT");
        grid.driveController.set_velocity(velocitySliderR.value, "RIGHT");
    }

    Keys.onRightPressed: event => {
        if (event.isAutoRepeat || !rightCheck.checked || !leftCheck.checked)
            return;
        rightButton.state = "ACTIVE";
        grid.driveController.set_velocity(velocitySliderL.value, "LEFT");
        grid.driveController.set_velocity(velocitySliderR.value * -1, "RIGHT");
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
        if (leftCheck.checked) {
            grid.driveController.set_velocity(0, "LEFT");
        }
        if (rightCheck.checked) {
            grid.driveController.set_velocity(0, "RIGHT");
        }
    }

    ColumnLayout {
        Layout.preferredWidth: 3
        RowLayout {
            CheckBox {
                id: leftCheck
                text: qsTr("Left")
                onToggled: () => {
                    PlotJS.resetPlot(chartL);
                    PlotJS.initSeries(chartL, xAxisL, yAxisL, "Left");
                    if (leftCheck.checked) {
                        grid.driveController.enable_motor("LEFT");
                    } else {
                        grid.driveController.disable_motor("LEFT");
                    }
                }
            }
            CheckBox {
                id: rightCheck
                text: qsTr("Right")
                onToggled: () => {
                    PlotJS.resetPlot(chartR);
                    PlotJS.initSeries(chartR, xAxisR, yAxisR, "Right");
                    if (rightCheck.checked) {
                        grid.driveController.enable_motor("RIGHT");
                    } else {
                        grid.driveController.disable_motor("RIGHT");
                    }
                }
            }
        }
        RowLayout {

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredHeight: 2
                ChartView {
                    id: chartL
                    anchors.fill: parent
                    axes: [
                        ValueAxis {
                            id: xAxisL
                            min: 1.0
                            max: 20.0
                        },
                        ValueAxis {
                            id: yAxisL
                            min: -7.5
                            max: 7.5
                        }
                    ]
                }
            }
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredHeight: 2
                ChartView {
                    id: chartR
                    anchors.fill: parent
                    axes: [
                        ValueAxis {
                            id: xAxisR
                            min: 1.0
                            max: 20.0
                        },
                        ValueAxis {
                            id: yAxisR
                            min: -7.5
                            max: 7.5
                        }
                    ]
                }
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
            text: "Max Velocity L"
        }
        Slider {
            id: velocitySliderL
            Layout.fillWidth: true
            from: 1
            to: 10
            value: 5
            onMoved: () => {
                PlotJS.setMaxVelocity(chartL, velocitySliderL.value);
            }
        }
        Text {
            Layout.fillWidth: true
            color: "black"
            text: "Max Velocity R"
        }
        Slider {
            id: velocitySliderR
            Layout.fillWidth: true
            from: 1
            to: 10
            value: 5
            onMoved: () => {
                PlotJS.setMaxVelocity(chartR, velocitySliderR.value);
            }
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
