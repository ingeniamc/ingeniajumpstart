pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts
import qmltypes.controllers 1.0
import "components" as Components

ApplicationWindow {
    id: page
    title: qsTr("Ingeniajumpstart")
    width: 800
    height: 600
    visible: true
    required property DriveController driveController

    Connections {
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
        sequence: "F12"
        context: Qt.ApplicationShortcut
        autoRepeat: false
        onActivated: () => page.driveController.emergency_stop()
    }

    Dialog {
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
        id: stack
        initialItem: selectionPage
        anchors.fill: parent
        focus: true
    }

    SelectionPage {
        id: selectionPage
        visible: false
        driveController: page.driveController
    }

    ControlsPage {
        id: controlsPage
        visible: false
        driveController: page.driveController
    }
}
