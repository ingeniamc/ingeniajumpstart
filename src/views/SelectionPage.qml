pragma ComponentBehavior: Bound
import QtQuick.Layouts
import QtQuick.Controls
import "components"
import QtQuick.Controls.Material

ColumnLayout {
    id: grid
    signal startButtonPressed

    RowLayout {
        SpacerW {
        }
        ComboBox {
            model: ["EtherCAT", "CANopen"]
            Layout.fillWidth: true
            Layout.preferredWidth: 1

            onActivated: {
                if (currentValue === "EtherCAT") {
                    compA.visible = false;
                } else {
                    compA.visible = true;
                }
            }
        }
        Button {
            text: "Scan"
            Layout.fillWidth: true
            Layout.preferredWidth: 1
        }
        SpacerW {
        }
    }
    RowLayout {
        SpacerW {
        }
        TextField {
            id: compA
            visible: false
            text: "Component A"
            Layout.fillWidth: true
            Layout.preferredWidth: 1
        }
        SpacerW {
        }
    }
    RowLayout {
        SpacerW {
        }
        TextField {
            id: compB
            text: "Component B"
            Layout.fillWidth: true
            Layout.preferredWidth: 1
        }
        SpacerW {
        }
    }

    RowLayout {
        SpacerW {
        }
        Button {
            text: "Start"
            Material.background: Material.Green
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            onClicked: () => grid.startButtonPressed()
        }
        SpacerW {
        }
    }
}
