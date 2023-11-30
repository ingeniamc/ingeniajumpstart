pragma ComponentBehavior: Bound
import QtQuick.Layouts
import "components" as Components
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
            const servo_ids_model = servo_ids.map((servo_id) => { return {
                value: servo_id,
                text: servo_id
            }});
            idLeftAutomatic.model = servo_ids_model;
            idRightAutomatic.model = servo_ids_model;
            idRightAutomatic.incrementCurrentIndex();
            idLeftAutomatic.enabled = true;
            idRightAutomatic.enabled = true;
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

    Components.Selection {
        text: "Select connection mode:"
        model: [{
                value: Enums.Connection.CANopen,
                text: "CANopen"
            }, {
                value: Enums.Connection.EtherCAT,
                text: "EtherCAT"
            }]
        activatedHandler: currentValue => {
            selectionPage.driveController.select_connection(currentValue);
            selectCANdevice.visible = currentValue == Enums.Connection.CANopen;
            selectBaudrate.visible = currentValue == Enums.Connection.CANopen;
            selectNetworkAdapter.visible = currentValue == Enums.Connection.EtherCAT;
            idLeftAutomatic.model = [];
            idRightAutomatic.model = [];
            idLeftAutomatic.enabled = false;
            idRightAutomatic.enabled = false;
        }
    }

    Components.Selection {
        id: selectNetworkAdapter
        text: "Select network adapter:"
        model: []
        visible: false
        Component.onCompleted: () => {
            const interface_name_list = selectionPage.driveController.get_interface_name_list();
            selectNetworkAdapter.model = interface_name_list.map((interface_name, index) => {
                    return {
                        value: index,
                        text: interface_name
                    };
                });
        }
        activatedHandler: currentValue => selectionPage.driveController.select_interface(currentValue)
    }

    Components.Selection {
        id: selectCANdevice
        text: "Select CAN device:"
        model: [{
                value: Enums.CanDevice.KVASER,
                text: "KVASER"
            }, {
                value: Enums.CanDevice.PCAN,
                text: "PCAN"
            }, {
                value: Enums.CanDevice.IXXAT,
                text: "IXXAT"
            }]
        activatedHandler: currentValue => selectionPage.driveController.select_can_device(currentValue)
    }

    Components.Selection {
        id: selectBaudrate
        text: "Select baudrate:"
        model: [{
                value: Enums.CAN_BAUDRATE.Baudrate_1M,
                text: "1 Mbit/s"
            }, {
                value: Enums.CAN_BAUDRATE.Baudrate_500K,
                text: "500 Kbit/s"
            }, {
                value: Enums.CAN_BAUDRATE.Baudrate_250K,
                text: "250 Kbit/s"
            }, {
                value: Enums.CAN_BAUDRATE.Baudrate_125K,
                text: "125 Kbit/s"
            }, {
                value: Enums.CAN_BAUDRATE.Baudrate_100K,
                text: "100 Kbit/s"
            }, {
                value: Enums.CAN_BAUDRATE.Baudrate_50K,
                text: "50 Kbit/s"
            }]
        activatedHandler: currentValue => selectionPage.driveController.select_can_baudrate(currentValue)
    }

    RowLayout {
        id: idsManual
        Components.SpacerW {
        }
        Text {
            text: "ID Left:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 4
            color: "#e0e0e0"
        }
        SpinBox {
            id: idLeft
            Layout.fillWidth: true
            Layout.preferredWidth: 4
            from: 0
            editable: true
            onValueModified: () => selectionPage.driveController.select_node_id(value, Enums.Drive.Left)
        }
        Components.SpacerW {
        }
        Text {
            text: "ID Right:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 4
            color: "#e0e0e0"
        }
        SpinBox {
            id: idRight
            Layout.fillWidth: true
            Layout.preferredWidth: 4
            from: 0
            editable: true
            onValueModified: () => selectionPage.driveController.select_node_id(value, Enums.Drive.Right)
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        id: idsAutomatic
        visible: false
        Components.SpacerW {
        }
        Text {
            text: "ID Left:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            color: "#e0e0e0"
        }
        ComboBox {
            id: idLeftAutomatic
            textRole: "text"
            valueRole: "value"
            enabled: false
            model: []
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Material.foreground: Material.foreground
            onActivated: () => selectionPage.driveController.select_node_id(currentValue, Enums.Drive.Left)
        }
        Components.SpacerW {
        }
        Text {
            text: "ID Right:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            color: "#e0e0e0"
        }
        ComboBox {
            id: idRightAutomatic
            textRole: "text"
            valueRole: "value"
            enabled: false
            model: []
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Material.foreground: Material.foreground
            onActivated: () => selectionPage.driveController.select_node_id(currentValue, Enums.Drive.Right)
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        id: scanBtn
        Components.SpacerW {
        }
        Components.Button {
            text: "Scan for IDs.."
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            onClicked: () => {
                selectionPage.driveController.scan_servos();
                manualBtn.visible = true
                scanBtn.visible = false
                idsAutomatic.visible = true
                idsManual.visible = false
            }
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        id: manualBtn
        visible: false
        Components.SpacerW {
        }
        Components.Button {
            text: "Select IDs manually.."
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            onClicked: () => {
                manualBtn.visible = false
                scanBtn.visible = true
                idsAutomatic.visible = false
                idsManual.visible = true
            }
        }
        Components.SpacerW {
        }
        Components.Button {
            text: "Scan"
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Material.background: '#007acc'
            Material.foreground: '#FFFFFF'
            hoverColor: '#85ceff'
            onClicked: () => {
                selectionPage.driveController.scan_servos();
            }
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        Components.SpacerW {
        }
        ColumnLayout {
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Components.Button {
                text: "Choose dictionary file..."
                onClicked: fileDialog.open()
            }
            Text {
                id: dictionaryFile
                color: '#e0e0e0'
                Layout.alignment: Qt.AlignHCenter
            }
        }
        Components.SpacerW {
        }
    }


    RowLayout {
        Components.SpacerW {
        }
        Components.Button {
            id: connectBtn
            text: "Connect"
            Material.background: '#2ffcab'
            Material.foreground: '#1b1b1b'
            hoverColor: '#acfedd'
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            state: Enums.ButtonState.Disabled
            states: [
                State {
                    name: Enums.ButtonState.Enabled
                    PropertyChanges {
                        target: connectBtn
                        enabled: true
                    }
                },
                State {
                    name: Enums.ButtonState.Disabled
                    PropertyChanges {
                        target: connectBtn
                        enabled: false
                    }
                }
            ]
            onClicked: () => {
                connectBtn.state = Enums.ButtonState.Disabled;
                selectionPage.driveController.connect();
            }
        }
        Components.SpacerW {
        }
    }
}
