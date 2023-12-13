pragma ComponentBehavior: Bound
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material
import qmltypes.controllers 1.0
import "../js/controls.js" as ControlsJS

// QEnum() does not seem to work properly with qmllint,
// which is why we disable this warning for this file.
// This only applies to the usage of Enums, if that is
// no longer used, the warning can be re-enabled.
// qmllint disable missing-property

Button {
    id: stateButton
    state: Enums.ButtonState.Disabled
    highlighted: false
    property int leftFactor
    property int rightFactor
    states: [
        State {
            name: Enums.ButtonState.Enabled
            PropertyChanges {
                target: stateButton
                highlighted: false
                enabled: true
            }
        },
        State {
            name: Enums.ButtonState.Active
            PropertyChanges {
                target: stateButton
                highlighted: true
                enabled: true
            }
        },
        State {
            name: Enums.ButtonState.Disabled
            PropertyChanges {
                target: stateButton
                highlighted: false
                enabled: false
            }
        }
    ]
    Action {
        shortcut: Qt.Key_Up
        onTriggered: () => console.log("and action")
    }
    onPressed: () => ControlsJS.handleButtonPressed(stateButton, leftFactor, rightFactor)
    onReleased: () => ControlsJS.handleButtonReleased(stateButton)
}
