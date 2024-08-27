pragma ComponentBehavior: Bound
import QtQuick.Layouts
import "components" as Components
import QtQuick.Controls.Material
import qmltypes.controllers 1.0
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs
import "js/selection.js" as SelectionJS

// QEnum() does not seem to work properly with qmllint,
// which is why we disable this warning for this file.
// This only applies to the usage of Enums, if that is
// no longer used, the warning can be re-enabled.
// qmllint disable missing-property

ColumnLayout {
    id: selectionPage
    required property ConnectionController connectionController

    property string dictionaryButtonMessage: "Choose dictionary"

    property string configurationButtonMessage: "(Optional) Choose config"
    
    Connections {
        target: selectionPage.connectionController
        function onDictionary_changed(dictionary, drive) {
            switch (drive) {
                case Enums.Drive.Axis1:
                    leftDictionaryUploadBtn.setFile(dictionary);
                    break;
                case Enums.Drive.Axis2:
                    rightDictionaryUploadBtn.setFile(dictionary);
                    break;
                case Enums.Drive.Both:
                    combinedDictionaryUploadBtn.setFile(dictionary);
                    break;
            }
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
            idsAutomatic.visible = true;
        }
        function onConfig_changed(config, drive) {
            switch (drive) {
                case Enums.Drive.Axis1:
                    leftConfigUploadBtn.setFile(config);
                    break;
                case Enums.Drive.Axis2:
                    rightConfigUploadBtn.setFile(config);
                    break;
                case Enums.Drive.Both:
                    combinedConfigUploadBtn.setFile(config);
                    break;
            }
        }
    }

    FileDialog {
        // Input for dictionary file.
        id: dictionaryfileDialog
        title: "Please choose a file"
        defaultSuffix: "xdf"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Dictionary files (*.xdf)"]
        property int drive
        onAccepted: {
            selectionPage.connectionController.select_dictionary(selectedFile, dictionaryfileDialog.drive);
        }
    }

    FileDialog {
        // Input for config file.
        id: configFileDialog
        title: "Please choose a file"
        defaultSuffix: "lfu"
        fileMode: FileDialog.OpenFile
        nameFilters: ["XCF Files (*.xcf)"]
        property int drive
        onAccepted: {
            selectionPage.connectionController.select_config(selectedFile, configFileDialog.drive);
        }
    }

    Components.Selection {
        text: "Select connection mode:"
        model: [{
                value: Enums.ConnectionProtocol.CANopen,
                text: "CANopen"
            }, {
                value: Enums.ConnectionProtocol.EtherCAT,
                text: "EtherCAT"
            }]
        activatedHandler: currentValue => {
            selectionPage.connectionController.select_connection(currentValue);
            selectCANdevice.visible = currentValue == Enums.ConnectionProtocol.CANopen;
            selectBaudrate.visible = currentValue == Enums.ConnectionProtocol.CANopen;
            selectNetworkAdapter.visible = currentValue == Enums.ConnectionProtocol.EtherCAT;
            idLeftAutomatic.model = [];
            idRightAutomatic.model = [];
            idLeftAutomatic.enabled = false;
            idRightAutomatic.enabled = false;
            SelectionJS.resetUploads(separateDictionariesBtn.checked, Components.UploadButton.FileType.Dictionary);
        }
    }

    Components.Selection {
        id: selectNetworkAdapter
        text: "Select network adapter:"
        model: []
        visible: false
        Component.onCompleted: () => {
            const interface_name_list = selectionPage.connectionController.get_interface_name_list();
            selectNetworkAdapter.model = interface_name_list.map((interface_name) => {
                    return {
                        value: interface_name,
                        text: interface_name
                    };
                });
        }
        activatedHandler: currentValue => selectionPage.connectionController.select_interface(currentValue)
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
        activatedHandler: currentValue => selectionPage.connectionController.select_can_device(currentValue)
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
        activatedHandler: currentValue => selectionPage.connectionController.select_can_baudrate(currentValue)
    }

    RowLayout {
        Components.SpacerW {
        }
        Text {
            text: "Connection mode:"
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            color: "#e0e0e0"
        }
        ComboBox {
            id: control
            textRole: "text"
            valueRole: "value"
            model: [{
                value: "Scan",
                text: "Scan"
            },
            {
                value: "Manual",
                text: "Manual"
            }]
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Material.foreground: Material.foreground
            onActivated: () => {
                scanButton.visible = (currentValue == "Scan");
                idsAutomatic.visible = (currentValue == "Scan" && idLeftAutomatic.model?.length > 0);
                idsManual.visible = (currentValue == "Manual");
            }
        }
        Components.SpacerW {
        }
        Components.StyledButton {
            id: scanButton
            text: "Scan"
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            Material.background: '#007acc'
            Material.foreground: '#FFFFFF'
            hoverColor: '#85ceff'
            onClicked: () => {
                selectionPage.connectionController.scan_servos();
            }
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        // Manual input for slave / node IDs.
        id: idsManual
        visible: false
        Components.SpacerW {
        }
        Text {
            text: "Axis 1 ID:"
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
            onValueModified: () => selectionPage.connectionController.select_node_id(value, Enums.Drive.Axis1)
        }
        Components.SpacerW {
        }
        Text {
            text: "Axis 2 ID:"
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
            onValueModified: () => selectionPage.connectionController.select_node_id(value, Enums.Drive.Axis2)
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        // Slave / node IDs returned from a scan.
        id: idsAutomatic
        visible: false
        Components.SpacerW {
        }
        Text {
            text: "Axis 1 ID:"
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
            onActivated: () => selectionPage.connectionController.select_node_id(currentValue, Enums.Drive.Axis1)
        }
        Components.SpacerW {
        }
        Text {
            text: "Axis 2 ID:"
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
            onActivated: () => selectionPage.connectionController.select_node_id(currentValue, Enums.Drive.Axis2)
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        // Switch to change whether to upload separate or combined configurations for each drive.
        Components.SpacerW {
        }
        Switch {
            id: separateConfigurationsBtn
            text: qsTr("Separate configurations")
            onClicked: () => {
                SelectionJS.resetUploads(separateConfigurationsBtn.checked, Components.UploadButton.FileType.Config);
            }
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        // Button for config file upload & display of currently selected file,
        // as well as a button to clear the config file. File will count for both drives.
        id: combinedConfigUpload
        Components.SpacerW {
        }
        Components.UploadButton {
            id: combinedConfigUploadBtn
            drive: Enums.Drive.Both
            fileType: Components.UploadButton.FileType.Config
            text: selectionPage.configurationButtonMessage
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        // Buttons for config file upload & display of currently selected files,
        // as well as a button to clear the config files. Separate buttons for each drive.
        id: separateConfigUpload
        visible: false
        Components.SpacerW {
        }
        Components.UploadButton {
            id: leftConfigUploadBtn
            drive: Enums.Drive.Axis1
            fileType: Components.UploadButton.FileType.Config
            text: selectionPage.configurationButtonMessage + " axis 1"
        }
        Components.SpacerW {
        }
        Components.UploadButton {
            id: rightConfigUploadBtn
            drive: Enums.Drive.Axis2
            fileType: Components.UploadButton.FileType.Config
            text: selectionPage.configurationButtonMessage + " axis 2"
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        // Switch to change whether to upload separate or combined dictionaries for each drive.
        Components.SpacerW {
        }
        Switch {
            id: separateDictionariesBtn
            text: qsTr("Separate dictionaries")
            onClicked: () => {
                SelectionJS.resetUploads(separateDictionariesBtn.checked, Components.UploadButton.FileType.Dictionary);
            }
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        // Button for dictionary file upload & display of currently selected file.
        // File will count for both drives.
        id: combinedDictionaryUpload
        Components.SpacerW {
        }
        Components.UploadButton {
            id: combinedDictionaryUploadBtn
            drive: Enums.Drive.Both
            fileType: Components.UploadButton.FileType.Dictionary
            text: selectionPage.dictionaryButtonMessage
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        // Buttons for dictionary file upload & display of currently selected files,
        // as well as a button to clear the dictionary files. Separate buttons for each drive.
        id: separateDictionaryUpload
        visible: false
        Components.SpacerW {
        }
        Components.UploadButton {
            id: leftDictionaryUploadBtn
            drive: Enums.Drive.Axis1
            fileType: Components.UploadButton.FileType.Dictionary
            text: selectionPage.dictionaryButtonMessage + " axis 1"
        }
        Components.SpacerW {
        }
        Components.UploadButton {
            id: rightDictionaryUploadBtn
            drive: Enums.Drive.Axis2
            fileType: Components.UploadButton.FileType.Dictionary
            text: selectionPage.dictionaryButtonMessage + " axis 2"
        }
        Components.SpacerW {
        }
    }

    RowLayout {
        Components.SpacerW {
        }
        Components.StyledButton {
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
                selectionPage.connectionController.connect();
            }
        }
        Components.SpacerW {
        }
    }
}
