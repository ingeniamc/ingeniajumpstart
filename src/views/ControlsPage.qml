pragma ComponentBehavior: Bound
import QtQuick.Layouts
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material
import "components"

RowLayout {
    id: grid
    signal cancelButtonPressed
    Keys.onUpPressed: event => {
        upButton.state = "ACTIVE";
    }
    Keys.onDownPressed: event => {
        downButton.state = "ACTIVE";
    }
    Keys.onLeftPressed: event => {
        leftButton.state = "ACTIVE";
    }
    Keys.onRightPressed: event => {
        rightButton.state = "ACTIVE";
    }
    Keys.onReleased: event => {
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
    }

    ColumnLayout {
        Layout.preferredWidth: 3

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: 2
            Text {
                color: "black"
                text: "Some amazing graphic"
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.fill: parent
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
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
            Layout.fillWidth: true
            value: 0.5
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
