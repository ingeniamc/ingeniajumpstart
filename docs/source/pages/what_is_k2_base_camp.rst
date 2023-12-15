*********************
What is K2 Base Camp?
*********************

K2 Base Camp is designed to be a simple application that allows you to quickly connect to your K2 drive and get the servo motors moving.

It is an open source application that is meant to serve as a demo that can be a starting point for the development of a more complex application.

.. WARNING::
    The drive and motors need to be configured and tuned using the `MotionLab3 <https://www.celeramotion.com/resources/videos/motionlab3-overview>`_ software before connecting with K2 Base Camp.

Features
========

At its core, it is a minimal interface that lets you connect to both drives of the K2 simultaneously using one of two connection protocols (`EtherCAT <https://en.wikipedia.org/wiki/EtherCAT>`_ and `CANopen <https://en.wikipedia.org/wiki/CANopen>`_).

You can then enable / disable the servo motors and get them moving using the arrow keys (or pressing the corresponding buttons).

The graphs will display the velocity of the motors over time, and the input box and sliders can be used to set additional parameters related to the velocity of the motors.