epaper telegram
===================

Communicate between 2 `waveshare touch epaper device <https://www.waveshare.com/wiki/2.13inch_Touch_e-Paper_HAT_Manual#Overview>`_!  One party draws a sketch or write a msg on the epaper display and can send it to its partner, which receive it immediately! Both devices need to be connected to internet.

TODO: add some pictures

hardware requirements
=======================

- a pair of waveshare touch epaper display (currently only the 2.13 inch is supported)
- a pair of raspberry pi

Installation
============


connect the epaper touch display to each raspberry pi. Make sur the raspberry pies are connected to the internet. Then on each raspberry pi you have to do the following steps:


be sure that you have activated the spi and i2c interface. On the raspberry pi:

.. code-block:: bash

    sudo raspi-config nonint do_spi 1
    sudo raspi-config nonint do_i2c 1

make sure you can create a virtual environment:

.. code-block:: bash

    sudo apt-get install python3-pip
    sudo apt-get install python3-venv

create a virtual environement and install the package:

.. code-block:: bash
   python3 -m venv epaper-telegram
   source epaper-telegram/bin/activate
   pip install git+https://github.com/ImamAzim/epaper-telegram.git

run the script to configure the app::

.. code-block:: bash
   epaper-telegram

configuration
______________



hardware requirements
=======================
* rpi
* waveshare

Usage
=====



Features
========

* receive messages
* draw and send


License
=======

The project is licensed under GNU GENERAL PUBLIC LICENSE v3.0
