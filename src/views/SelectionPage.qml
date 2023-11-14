pragma ComponentBehavior: Bound
import QtQuick.Layouts
import "components"
import QtQuick.Controls.Material
import qmltypes.controllers 1.0
import QtQuick 2.15
import QtQuick.Controls 2.15

ColumnLayout {
    id: selectionPage
    required property DriveController driveController

    Connections {
        target: selectionPage.driveController
        function onDriveDisconnected() {
            connectBtn.state = "NORMAL";
        }
    }

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
            id: connectBtn
            text: "Connect"
            Material.background: Material.Green
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            state: "NORMAL"
            states: [
                State {
                    name: "NORMAL"
                    PropertyChanges {
                        target: connectBtn
                        enabled: true
                    }
                },
                State {
                    name: "LOADING"
                    PropertyChanges {
                        target: connectBtn
                        enabled: false
                    }
                }
            ]
            onClicked: () => {
                connectBtn.state = "LOADING";
                selectionPage.driveController.connect();
            }
        }
        SpacerW {
        }
    }
}
