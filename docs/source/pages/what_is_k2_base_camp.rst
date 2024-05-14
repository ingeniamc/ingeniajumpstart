*********************
What is K2 Base Camp?
*********************

**K2 Base Camp** is designed to be a simple application that allows you to quickly connect to your K2 drive and get the servo motors moving.

It is an open source application that is meant to serve as a demo that can be a starting point for the development of a more complex application.

.. WARNING::
    The drive and motors need to be configured and tuned using the `MotionLab3 <https://www.celeramotion.com/resources/videos/motionlab3-overview>`_ software before connecting with **K2 Base Camp**.

Features
========

At its core, **K2 Base Camp** is a minimal interface that lets you connect to both drives of the K2 simultaneously using one of two communication protocols (`EtherCAT <https://en.wikipedia.org/wiki/EtherCAT>`_ and `CANopen <https://en.wikipedia.org/wiki/CANopen>`_).

You also have the option to provide files with configurations for the drives that are loaded when you make the connection.

You can then enable / disable the servo motors and get them moving using the arrow keys (or pressing the corresponding buttons).

The interface includes a LED for each motor that displays its current status (**Red** = Disabled, **Yellow** = Ready, **Green** = Enabled).

Graphs display the velocity of the motors over time, and the input boxes and sliders can be used to set additional parameters related to the velocity of the motors.

Usage
=====

The application is divided into three pages - a "Bootloader"-page to install firmware, a "Connection"-page to connect to the drive, and a "Controls"-page where you can enable and move the motors.

Connection Page
---------------

Upon opening the application, this is the first page that is shown. The purpose of this page is to connect to the drives.

#. Select a connection protocol:

    .. image:: ../_static/connection_page_select_protocol.png
                :width: 400
                :alt: Connection page with connection mode dropdown highlighted

#. Set additonal parameters needed for the connection:

    .. image:: ../_static/connection_page_select_adapter.png
                :width: 400
                :alt: Connection page with network adapter dropdown highlighted

#. Scan for the drives in the network (you can also enter the nodes manually):

    .. image:: ../_static/connection_page_scan.png
                :width: 400
                :alt: Connection page with scan button highlighted

#. (Optional) Select configuration files for the drives. If you want to use separate configuration for the drives, enable the "Separate configurations" switch:

    .. image:: ../_static/connection_page_config.png
                :width: 400
                :alt: Connection page with configuration switch and configuration file upload highlighted

#. Select the dictionary for the drives. If you want to use separate dictionaries for the drives, enable the "Separate dictionaries" switch:

    .. image:: ../_static/connection_page_dictionary.png
                :width: 400
                :alt: Connection page with dictionary file upload highlighted

#. Hit the "Connect" button:

    .. image:: ../_static/connection_page_connect.png
                :width: 400
                :alt: Connection page with active connect button highlighted

Controls Page
-------------

Upon connecting, the "Controls"-page opens where you can start moving the motors.

#. Check one of the "Enable motor"-boxes to enable the corresponding motor:

    .. image:: ../_static/controls_page_enable_motors.png
                :width: 400
                :alt: Controls page with enable motor button highlighted

#. The LED next to the checkbox will inform you about the state of the motor:

    .. image:: ../_static/controls_page_led.png
                :width: 400
                :alt: Controls page with LED highlighted

#. The current velocity will be plotted while the motor is active:

    .. image:: ../_static/controls_page_plot.png
                :width: 400
                :alt: Controls page with plot highlighted

#. Use the arrow keys or buttons at the bottom to move the motor (left/right is only available if both motors are enabled):

    .. image:: ../_static/controls_page_keys.png
                :width: 400
                :alt: Controls page with arrow key buttons highlighted

#. The input fields and sliders at the right can be used to set the maximum and target velocities (keep in mind that the actual velocity your motor reaches will be dependent on the drive):

    .. image:: ../_static/controls_page_sliders.png
                :width: 400
                :alt: Controls page with sliders highlighted

#. Hitting the "Disconnect"-button will take you back to the "Connection"-page:

    .. image:: ../_static/controls_page_disconnect.png
                :width: 400
                :alt: Controls page with disconnect button highlighted

Bootloader Page
---------------

Pressing the "Bootloader"-button on the "Connection"-page will take you to this page. Here you can install a different firmware to the drives using a .zfu file.

#. Prepare to connect to the drives just as you do on the "Connection"-page:

    .. image:: ../_static/bootloader_page_configure.png
                :width: 400
                :alt: Bootloader page with configuration dropdowns highlighted

#. Upload a .zfu-file using the "Choose firmware.."-button:

    .. image:: ../_static/bootloader_page_firmware.png
                :width: 400
                :alt: Bootloader page with firmware file upload highlighted

#. Hit the "Load firmware"-button and confirm the operation in the dialog:

    .. image:: ../_static/bootloader_page_load_firmware.png
                :width: 400
                :alt: Bootloader page with load firwmware button highlighted
                
    .. image:: ../_static/bootloader_page_confirm_dialog.png
                :width: 400
                :alt: Bootloader page confirmation dialog

#. A dialog will appear once the installation completes to confirm the successful operation:

    .. image:: ../_static/bootloader_page_progress.png
                :width: 400
                :alt: Bootloader page installation in progress

    .. image:: ../_static/bootloader_page_success_dialog.png
                :width: 400
                :alt: Bootloader page installation completed dialog