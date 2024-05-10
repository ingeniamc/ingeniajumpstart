/**
 * Reset the upload button components used for file uploads and display separate or combined buttons as
 * desired by the user.
 * @param {boolean} selectSeparately 
 * @param {Components.UploadButton.FileType} fileType 
 */
function resetUploads(selectSeparately, fileType) {
    switch (fileType) {
        case Components.UploadButton.FileType.Config:
            setSelectSeparately(combinedConfigUpload, separateConfigUpload, selectSeparately);
            selectionPage.connectionController.reset_config(Enums.Drive.Both);
            resetUploadButtons([combinedConfigUploadBtn, leftConfigUploadBtn, rightConfigUploadBtn]);
            break;
        case Components.UploadButton.FileType.Dictionary:
            setSelectSeparately(combinedDictionaryUpload, separateDictionaryUpload, selectSeparately);
            selectionPage.connectionController.reset_dictionary(Enums.Drive.Both);
            resetUploadButtons([combinedDictionaryUploadBtn, leftDictionaryUploadBtn, rightDictionaryUploadBtn]);
            break;
    }
}

/**
 * Sets the interface to display either separate or combined upload buttons.
 * @param {RowLayout} combinedUploadComponent 
 * @param {RowLayout} separateUploadComponent 
 * @param {boolean} selectSeparately 
 */
function setSelectSeparately(combinedUploadComponent, separateUploadComponent, selectSeparately) {
    combinedUploadComponent.visible = !selectSeparately;
    separateUploadComponent.visible = selectSeparately;
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