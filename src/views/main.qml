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

    required property MainWindowController mainWindowController
    required property MainWindowConsole mainWindowConsole
    Connections {
        target: page.mainWindowController
        function onValueChanged(val) {
            stack.rotation = val;
        }
    }
    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            ToolButton {
                enabled: stack.depth > 1
                text: qsTr("‹")
                onClicked: stack.pop()
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
        onStartButtonPressed: () => stack.push(controlsPage)
    }

    ControlsPage {
        id: controlsPage
        visible: false
        onCancelButtonPressed: () => stack.pop()
    }
}
