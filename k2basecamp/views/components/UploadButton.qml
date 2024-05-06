pragma ComponentBehavior: Bound
import QtQuick.Layouts
import QtQuick.Controls.Material
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window

// The linter struggles with seeing references to the parent component.
// qmllint disable unqualified

// Helper component to abstract some of the logic 
// for uploading files.

ColumnLayout {
    id: uploadComponent

    Layout.fillWidth: true
    Layout.preferredWidth: 2

    enum FileType {
        Config,
        Dictionary
    }

    property int fileType
    property int drive


    function resetUpload() {
        fileText.text = "";
        resetBtn.visible = false;
        uploadBtn.enabled = true;
    }

    function setFile(file) {
        const hasFile = (file === "");
        fileText.text = file;
        resetBtn.visible = !hasFile;
        uploadBtn.enabled = hasFile;
    }
    
    StyledButton {
        id: uploadBtn
        text: "(Optional) Choose config..."
        onClicked: {
            switch (uploadComponent.fileType) {
                case UploadButton.FileType.Config:
                    configFileDialog.drive = drive
                    configFileDialog.open()
                    break;
                case UploadButton.FileType.Dictionary:
                    dictionaryfileDialog.drive = drive
                    dictionaryfileDialog.open()
                    break;
            }
        }
    }
    RowLayout {
        Layout.alignment: Qt.AlignHCenter
        Text {
            id: fileText
            color: '#e0e0e0'
        }
        RoundButton {
            id: resetBtn
            text: "X"
            visible: false
            onClicked: () => {
                switch (uploadComponent.fileType) {
                    case UploadButton.FileType.Config:
                        selectionPage.connectionController.reset_config(drive);
                        break;
                    case UploadButton.FileType.Dictionary:
                        selectionPage.connectionController.reset_dictionary(drive);
                        break;
                }
                resetBtn.visible = false;
                uploadBtn.enabled = true;
            }
        }
    }
}