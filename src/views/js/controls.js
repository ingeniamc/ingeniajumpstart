function handleButtonPressed(button, leftFactor, rightFactor, event) {
    if (event?.isAutoRepeat || button.state == Enums.ButtonState.Disabled)
        return;
    button.state = Enums.ButtonState.Active;
    if (leftCheck.checked) {
        grid.driveController.set_velocity(velocitySliderL.value * leftFactor, Enums.Drive.Left);
    }
    if (rightCheck.checked) {
        grid.driveController.set_velocity(velocitySliderR.value * rightFactor, Enums.Drive.Right);
    }
}

function handleButtonReleased(button) {
    if (button.state == Enums.ButtonState.Disabled)
        return;
    button.state = Enums.ButtonState.Enabled;
    if (leftCheck.checked) {
        grid.driveController.set_velocity(0, Enums.Drive.Left);
    }
    if (rightCheck.checked) {
        grid.driveController.set_velocity(0, Enums.Drive.Right);
    }
}

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