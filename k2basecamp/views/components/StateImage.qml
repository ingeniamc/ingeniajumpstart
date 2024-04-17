pragma ComponentBehavior: Bound
import QtQuick 2.15
import qmltypes.controllers 1.0

// QEnum() does not seem to work properly with qmllint,
// which is why we disable this warning for this file.
// This only applies to the usage of Enums, if that is
// no longer used, the warning can be re-enabled.
// qmllint disable missing-property

// Helper component to abstract some of the state logic 
// for displaying info about the drive.

Image {
    id: stateImage
    sourceSize.width: 20
    sourceSize.height: 20
    source: "images/circle-available.svg"
    state: Enums.SERVO_STATE.RDY
    states: [
        State {
            name: Enums.SERVO_STATE.RDY
            PropertyChanges {
                target: stateImage
                source: "images/circle-available.svg"
            }
        },
        State {
            name: Enums.SERVO_STATE.ENABLED
            PropertyChanges {
                target: stateImage
                source: "images/circle-enabled.svg"
            }
        },
        State {
            name: Enums.SERVO_STATE.DISABLED
            PropertyChanges {
                target: stateImage
                source: "images/circle-fault.svg"
            }
        }
    ]
}