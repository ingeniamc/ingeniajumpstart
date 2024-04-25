/**
 * Handler for arrow key buttons. Fires on pressing a button.
 * Sets the velocity of the motors to the given speeeds.
 * @param {Button} button 
 * @param {int} leftFactor 
 * @param {int} rightFactor 
 * @param {KeyEvent} event 
 */
function handleButtonPressed(button, leftFactor, rightFactor) {
    if (button.state != Enums.ButtonState.Enabled)
        return;

    // Reset all other buttons
    for (const otherButton of [upButton, downButton, leftButton, rightButton]) {
        if (button == otherButton || otherButton.state != Enums.ButtonState.Active) continue;
        otherButton.state = Enums.ButtonState.Enabled;
    }

    button.state = Enums.ButtonState.Active;
    if (leftCheck.checked) {
        grid.connectionController.set_velocity(velocitySliderL.value * leftFactor, Enums.Drive.Left);
    }
    if (rightCheck.checked) {
        grid.connectionController.set_velocity(velocitySliderR.value * rightFactor, Enums.Drive.Right);
    }
}

/**
 * Handler for arrow key buttons. Fires on releasing a button.
 * Sets the velocity of the motors to 0.
 * @param {Button} button 
 */
function handleButtonReleased(button) {
    if (button.state != Enums.ButtonState.Active)
        return;
    button.state = Enums.ButtonState.Enabled;
    if (leftCheck.checked) {
        grid.connectionController.set_velocity(0, Enums.Drive.Left);
    }
    if (rightCheck.checked) {
        grid.connectionController.set_velocity(0, Enums.Drive.Right);
    }
}

/**
 * Enable / disable arrow key buttons depending on the state of the motors:
 * No motors on - all disabled.
 * One motor on - up / down enabled, left / right disabled.
 * Both motors on - all enabled. 
 */
function updateKeyState() {
    if (leftCheck.checked || rightCheck.checked) {
        upButton.state = Enums.ButtonState.Enabled;
        downButton.state = Enums.ButtonState.Enabled;
    } else {
        upButton.state = Enums.ButtonState.Disabled;
        downButton.state = Enums.ButtonState.Disabled;
    }
    if (leftCheck.checked && rightCheck.checked) {
        leftButton.state = Enums.ButtonState.Enabled;
        rightButton.state = Enums.ButtonState.Enabled;
    } else {
        leftButton.state = Enums.ButtonState.Disabled;
        rightButton.state = Enums.ButtonState.Disabled;
    }
}

/**
 * Reset all the control elements of the interface to their initial state
 */
function resetControls() {
    leftCheck.checked = false;
    rightCheck.checked = false;
    for (const button of [upButton, downButton, leftButton, rightButton]) {
        button.state = Enums.ButtonState.Disabled
    }
}