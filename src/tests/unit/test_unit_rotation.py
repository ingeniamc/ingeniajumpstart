from controllers.main_window_controller import MainWindowController


def test_rotation() -> None:
    main_window_controller = MainWindowController()
    initial_rotation = main_window_controller.rotateValue.r
    main_window_controller.rotate()
    assert (initial_rotation + 10) == main_window_controller.rotateValue.r
