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
        function onDictionary_changed(dictionary) {
            dictionaryFile.text = dictionary;
        }
        function onConnect_button_state_changed(new_state) {
            connectBtn.state = new_state;
        }
        function onServo_ids_changed(servo_ids) {
            idLeft.value = servo_ids[0];
            idRight.value = servo_ids[1];
        }
    }

    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        defaultSuffix: "xdf"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Dictionary files (*.xdf)"]
        onAccepted: {
            selectionPage.driveController.select_dictionary(selectedFile);
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
                selectNetworkAdapter.visible = currentValue == Enums.Connection.EtherCAT;
            }
        }
        SpacerW {
        }
    }

    RowLayout {
        id: selectNetworkAdapter
        visible: false
        SpacerW {
        }
        Text {
            text: "Select network adapter:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 2
        }
        ComboBox {
            id: selectNetworkAdapterBox
            textRole: "text"
            valueRole: "value"
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Component.onCompleted: () => {
                const interface_name_list = selectionPage.driveController.get_interface_name_list();
                selectNetworkAdapterBox.model = interface_name_list.map((interface_name, index) => {
                        return {
                            value: index,
                            text: interface_name
                        };
                    });
            }
            onActivated: () => selectionPage.driveController.select_interface(currentValue)
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
        SpacerW {
        }
        Text {
            text: "ID Left:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 4
        }
        SpinBox {
            id: idLeft
            Layout.fillWidth: true
            Layout.preferredWidth: 4
            from: 0
            editable: true
            onValueModified: () => selectionPage.driveController.select_node_id(value, Enums.Drive.Left)
        }
        SpacerW {
        }
        Text {
            text: "ID Right:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 4
        }
        SpinBox {
            id: idRight
            Layout.fillWidth: true
            Layout.preferredWidth: 4
            from: 0
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
            id: scanBtn
            text: "Scan"
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            onClicked: () => {
                selectionPage.driveController.scan_servos();
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
            state: Enums.ConnectButtonState.Disabled
            states: [
                State {
                    name: Enums.ConnectButtonState.Enabled
                    PropertyChanges {
                        target: connectBtn
                        enabled: true
                    }
                },
                State {
                    name: Enums.ConnectButtonState.Disabled
                    PropertyChanges {
                        target: connectBtn
                        enabled: false
                    }
                }
            ]
            onClicked: () => {
                connectBtn.state = Enums.ConnectButtonState.Disabled;
                selectionPage.driveController.connect();
            }
        }
        SpacerW {
        }
    }
}
