/**
 * Reset the upload button components used for file uploads and display seperate or combined buttons as
 * desired by the user.
 * @param {boolean} selectSeperately 
 * @param {Components.UploadButton.FileType} fileType 
 */
function resetUploads(selectSeperately, fileType) {
    switch (fileType) {
        case Components.UploadButton.FileType.Config:
            setSelectSeperately(combinedConfigUpload, separateConfigUpload, selectSeperately);
            selectionPage.connectionController.reset_config(Enums.Drive.Both);
            resetUploadButtons([combinedConfigUploadBtn, leftConfigUploadBtn, rightConfigUploadBtn]);
            break;
        case Components.UploadButton.FileType.Dictionary:
            setSelectSeperately(combinedDictionaryUpload, separateDictionaryUpload, selectSeperately);
            selectionPage.connectionController.reset_dictionary(Enums.Drive.Both);
            resetUploadButtons([combinedDictionaryUploadBtn, leftDictionaryUploadBtn, rightDictionaryUploadBtn]);
            break;
    }
}

/**
 * Sets the interface to display either seperate or combined upload buttons.
 * @param {RowLayout} combinedUploadComponent 
 * @param {RowLayout} seperateUploadComponent 
 * @param {boolean} selectSeperately 
 */
function setSelectSeperately(combinedUploadComponent, seperateUploadComponent, selectSeperately) {
    combinedUploadComponent.visible = !selectSeperately;
    seperateUploadComponent.visible = selectSeperately;
}

/**
 * Calls a function on each given UploadButton that resets its interface.
 * @param {UploadButton[]} uploadButtons 
 */
function resetUploadButtons(uploadButtons) {
    for (const uploadButton of uploadButtons) {
        uploadButton.resetUpload();
    }
}