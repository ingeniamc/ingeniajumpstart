pragma ComponentBehavior: Bound
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material

Button {
    id: stateButton
    state: "NORMAL"
    highlighted: false

    states: [
        State {
            name: "NORMAL"
            PropertyChanges {
                target: stateButton
                highlighted: false
            }
        },
        State {
            name: "ACTIVE"
            PropertyChanges {
                target: stateButton
                highlighted: true
            }
        }
    ]
}
