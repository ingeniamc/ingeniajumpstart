import QtQuick
import QtQuick.Controls
import qmltypes.controllers 1.0
import "components"

Rectangle {
    id: page

    width: 500
    height: 200
    color: "lightgray"

    required property MainWindowController mainWindowController
    required property MainWindowConsole mainWindowConsole

    CustomComponent {
        id: helloText
    }

    ComboBox {
        model: ["First", "Second", "Third"]
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Connections {
        target: page.mainWindowController
        function onValueChanged(val) {
            helloText.rotation = val;
        }
    }

    Rectangle {
        id: button
        width: 150
        height: 40
        color: "darkgray"
        anchors.horizontalCenter: parent.horizontalCenter
        y: 120
        MouseArea {
            id: buttonMouseArea
            objectName: "buttonMouseArea"
            anchors.fill: parent
            onClicked: {
                // once the "console" context has been declared,
                // slots can be called like functions
                page.mainWindowConsole.outputFloat(123);
                page.mainWindowConsole.outputStr("foobar");
                page.mainWindowConsole.output(helloText.x);
                page.mainWindowConsole.output(helloText.text);
            }
        }
        Text {
            id: buttonText
            text: "Press me!"
            anchors.horizontalCenter: button.horizontalCenter
            anchors.verticalCenter: button.verticalCenter
            font.pointSize: 16
        }
    }
}
