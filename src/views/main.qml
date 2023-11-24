pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts
import qmltypes.controllers 1.0

ApplicationWindow {
    id: page
    title: qsTr("Ingeniajumpstart")
    width: 640
    height: 480
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
        RowLayout {
            anchors.fill: parent
            ToolButton {
                enabled: stack.depth > 1
                text: qsTr("‹")
                onClicked: () => page.driveController.disconnect()
                Layout.preferredWidth: 50
            }
            Label {
                text: stack.depth > 1 ? "Controls" : "Connection"
                elide: Label.ElideRight
                horizontalAlignment: Qt.AlignHCenter
                verticalAlignment: Qt.AlignVCenter
                Layout.fillWidth: true
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
