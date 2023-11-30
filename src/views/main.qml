pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts
import qmltypes.controllers 1.0

ApplicationWindow {
    id: page
    title: qsTr("Hello World")
    width: 640
    height: 480
    visible: true

    required property DriveController driveController

    Connections {
        target: page.driveController
        function onDriveConnected() {
            stack.push(controlsPage);
        }
        function onDriveDisconnected() {
            stack.pop();
        }
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
                text: "Title"
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
