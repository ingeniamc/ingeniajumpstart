/**
 * After selecting a firmware with the file dialog, this function updates the interface.
 * The name of the file is displayed and the button used to select a firmware file is disabled.
 * @param {str} firmware 
 */
function setFirmware(firmware) {
    firmwareFile.text = firmware;
    resetFirmware.visible = true;
    firmwareButton.enabled = false;
}

/**
 * Set the state of the GUI after a scan returned the ids of the drives in the network.
 * @param {int[]} servoIDs 
 */
function setServoIDs(servoIDs) {
    const servoIDsModel = servoIDs.map((servoID) => {
        return {
            value: servoID,
            text: servoID
        }
    });
    idLeftAutomatic.model = servoIDsModel;
    idLeftAutomatic.enabled = true;
    // Handle if the scan returned only one servo
    if (servoIDsModel.length > 1) {
        idRightAutomatic.model = servoIDsModel;
        idRightAutomatic.incrementCurrentIndex();
        idRightAutomatic.enabled = true;
    } else {
        idRightAutomatic.enabled = false;
    }
    idsAutomatic.visible = true;
}

/**
 * Resets the installation dialog.
 */
function resetDialog() {
    progressDialog.visible = false
    progressDialogBar.indeterminate = true;
    progressDialogButtons.visible = true
    isInProgress.visible = false
    installDialog.close();
}

/**
 * Updates the progress bar in the GUI when the installation progress gets updated.
 * @param {int[]} drives 
 */
function showInstallationProgress() {
    progressDialogButtons.visible = false
    isInProgress.visible = true
    progressDialog.visible = true
}