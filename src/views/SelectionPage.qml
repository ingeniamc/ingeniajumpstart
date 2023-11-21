pragma ComponentBehavior: Bound
import QtQuick.Layouts
import "components"
import QtQuick.Controls.Material
import qmltypes.controllers 1.0
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs

ColumnLayout {
    id: selectionPage
    required property DriveController driveController

    Connections {
        target: selectionPage.driveController
        function onDrive_disconnected_triggered() {
            connectBtn.state = "NORMAL";
        }
        function onDictionary_changed(dictionary) {
            dictionaryFile.text = dictionary;
        }
        function onConnection_error_triggered(error_message) {
            errorMessageDialogLabel.text = error_message;
            errorMessageDialog.open();
            connectBtn.state = "NORMAL";
        }
    }

    Dialog {
        id: errorMessageDialog
        modal: true
        title: qsTr("Connection failed")
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        Label {
            id: errorMessageDialogLabel
            text: "Lorem ipsum..."
        }
        standardButtons: Dialog.Ok
    }

    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        defaultSuffix: "xdf"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Dictionary files (*.xdf)"]
        onAccepted: {
            selectionPage.driveController.select_dictionary(selectedFile);
            connectBtn.state = "NORMAL";
        }
    }

    RowLayout {
        SpacerW {
        }
        Text {
            text: "Select connection mode:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 2
        }
        ComboBox {
            model: ["EtherCAT", "CANopen"]
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            onActivated: () => {
                selectionPage.driveController.select_connection(currentValue);
            }
        }
        SpacerW {
        }
    }
    RowLayout {
        SpacerW {
        }
        ColumnLayout {
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Button {
                text: qsTr("Choose dictionary file...")
                onClicked: fileDialog.open()
            }
            Text {
                id: dictionaryFile
                Layout.alignment: Qt.AlignHCenter
            }
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
            state: "DISABLED"
            states: [
                State {
                    name: "NORMAL"
                    PropertyChanges {
                        target: connectBtn
                        enabled: true
                    }
                },
                State {
                    name: "DISABLED"
                    PropertyChanges {
                        target: connectBtn
                        enabled: false
                    }
                }
            ]
            onClicked: () => {
                connectBtn.state = "DISABLED";
                selectionPage.driveController.connect();
            }
        }
        SpacerW {
        }
    }
}
