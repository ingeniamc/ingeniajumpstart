pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts
import qmltypes.controllers 1.0
import "components" as Components

ApplicationWindow {
    id: page
    title: qsTr("K2 Base Camp")
    width: 800
    height: 600
    visible: true
    required property DriveController driveController

    Connections {
        // Receive signals coming from the controllers.
        target: page.driveController
        function onDrive_connected_triggered() {
            if (stack.depth <= 1)
                stack.push(controlsPage);
        }
        function onDrive_disconnected_triggered() {
            stack.pop();
        }
        function onError_triggered(error_message) {
            errorMessageDialogLabel.text = error_message;
            errorMessageDialog.open();
        }
    }

    Shortcut {
        // Binds the emergency shutdown command to a keyboard key.
        sequence: "F12"
        context: Qt.ApplicationShortcut
        autoRepeat: false
        onActivated: () => page.driveController.emergency_stop()
    }

    Dialog {
        // Error messages are displayed in this dialog.
        id: errorMessageDialog
        modal: true
        title: qsTr("An error occured")
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        Label {
            id: errorMessageDialogLabel
        }
        standardButtons: Dialog.Ok
    }

    header: ToolBar {
        background: Rectangle {
            color: '#1b1b1b'
        }
        RowLayout {
            anchors.fill: parent
            ToolButton {
                id: backButton
                enabled: stack.depth > 1
                text: qsTr("‹")
                contentItem: Text {
                    text: backButton.text
                    font: backButton.font
                    opacity: enabled ? 1.0 : 0.3
                    color: backButton.down ? "#009688" : "#e0e0e0"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                }
                onClicked: () => page.driveController.disconnect()
                Layout.preferredWidth: 1
                Layout.fillWidth: true
            }
            Item {
                Layout.fillWidth: true
                Layout.preferredWidth: 8
            }

            Label {
                text: stack.depth > 1 ? "Controls" : "Connection"
                elide: Label.ElideRight
                horizontalAlignment: Qt.AlignHCenter
                verticalAlignment: Qt.AlignVCenter
                Layout.fillWidth: true
                Layout.preferredWidth: 4
                color: "#e0e0e0"
            }

            Item {
                Layout.fillWidth: true
                Layout.preferredWidth: 6
            }

            Components.Button {
                objectName: "emergencyStopBtn"
                text: "Stop (F12)"
                Layout.preferredWidth: 3
                Layout.fillWidth: true
                Material.background: '#b5341b'
                Material.foreground: '#ffffff'
                hoverColor: '#efa496'
                onClicked: () => page.driveController.emergency_stop()
            }
        }
    }

    StackView {
        // Handles multiple pages layout.
        id: stack
        initialItem: selectionPage
        anchors.fill: parent
        focus: true
    }

    SelectionPage {
        // The first page is an interface to establish the connection with the drive.
        id: selectionPage
        visible: false
        driveController: page.driveController
    }

    ControlsPage {
        // The second page is an interface that allows manipulating the velocity of the connected motors.
        id: controlsPage
        visible: false
        driveController: page.driveController
    }
}
