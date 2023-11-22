pragma ComponentBehavior: Bound
import QtQuick.Layouts
import "components"
import QtQuick.Controls.Material
import qmltypes.controllers 1.0
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs

// QEnum() does not seem to work properly with qmllint,
// which is why we disable this warning for this file.
// This only applies to the usage of Enums, if that is
// no longer used, the warning can be re-enabled.
// qmllint disable missing-property

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
            textRole: "text"
            valueRole: "value"
            model: [{
                    value: Enums.Connection.CANopen,
                    text: qsTr("CANopen")
                }, {
                    value: Enums.Connection.EtherCAT,
                    text: qsTr("EtherCAT")
                }]
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            onActivated: () => {
                selectionPage.driveController.select_connection(currentValue);
                selectCANdevice.visible = currentValue == Enums.Connection.CANopen;
                selectBaudrate.visible = currentValue == Enums.Connection.CANopen;
                selectNodeIDs.visible = currentValue == Enums.Connection.CANopen;
            }
        }
        SpacerW {
        }
    }

    RowLayout {
        id: selectCANdevice
        SpacerW {
        }
        Text {
            text: "Select CAN device:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 2
        }
        ComboBox {
            textRole: "text"
            valueRole: "value"
            model: [{
                    value: Enums.CanDevice.KVASER,
                    text: qsTr("KVASER")
                }, {
                    value: Enums.CanDevice.PCAN,
                    text: qsTr("PCAN")
                }, {
                    value: Enums.CanDevice.IXXAT,
                    text: qsTr("IXXAT")
                }]
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            onActivated: () => selectionPage.driveController.select_can_device(currentValue)
        }
        SpacerW {
        }
    }
    RowLayout {
        id: selectBaudrate
        SpacerW {
        }
        Text {
            text: "Select baudrate:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 2
        }
        ComboBox {
            textRole: "text"
            valueRole: "value"
            model: [{
                    value: Enums.CAN_BAUDRATE.Baudrate_1M,
                    text: qsTr("1 Mbit/s")
                }, {
                    value: Enums.CAN_BAUDRATE.Baudrate_500K,
                    text: qsTr("500 Kbit/s")
                }, {
                    value: Enums.CAN_BAUDRATE.Baudrate_250K,
                    text: qsTr("250 Kbit/s")
                }, {
                    value: Enums.CAN_BAUDRATE.Baudrate_125K,
                    text: qsTr("125 Kbit/s")
                }, {
                    value: Enums.CAN_BAUDRATE.Baudrate_100K,
                    text: qsTr("100 Kbit/s")
                }, {
                    value: Enums.CAN_BAUDRATE.Baudrate_50K,
                    text: qsTr("50 Kbit/s")
                }]
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            onActivated: () => selectionPage.driveController.select_can_baudrate(currentValue)
        }
        SpacerW {
        }
    }

    RowLayout {
        id: selectNodeIDs
        SpacerW {
        }
        Text {
            text: "Node ID Left:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 4
        }
        SpinBox {
            Layout.fillWidth: true
            Layout.preferredWidth: 4
            from: 0
            value: 31
            editable: true
            onValueModified: () => selectionPage.driveController.select_node_id(value, Enums.Drive.Left)
        }
        SpacerW {
        }
        Text {
            text: "Node ID Right:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 4
        }
        SpinBox {
            Layout.fillWidth: true
            Layout.preferredWidth: 4
            from: 0
            value: 32
            editable: true
            onValueModified: () => selectionPage.driveController.select_node_id(value, Enums.Drive.Right)
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
