pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts
import qmltypes.controllers 1.0

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
                Layout.preferredWidth: 50
            }
            Label {
                text: stack.depth > 1 ? "Controls" : "Connection"
                elide: Label.ElideRight
                horizontalAlignment: Qt.AlignHCenter
                verticalAlignment: Qt.AlignVCenter
                Layout.fillWidth: true
                color: "#e0e0e0"
            }
            Item {
                Layout.preferredWidth: 50
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
