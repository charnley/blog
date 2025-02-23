---
layout: post
title: "Setup automatic art, part 2"
date: 2025-01-25 18:09:47 +0100
categories: homeassistant ai art esp32 raspberry pi
published: false
---



From https://www.waveshare.com/wiki/E-Paper_ESP32_Driver_Board
Which is esp32-s3-devkitc-1


Rev 2.3 (9 pins, NOT 8 pins)

| PIN | Description |
| --- | --- | --- |
| VCC | Power positive (3.3V power supply input) |
| GND | Ground |
| DIN | SPI's MOSI, data input |
| CLK | SPI's SCK pin, clock signal input |
| CS | SPI Chip selection, low active |
| DC | Data/Command, low for command, high for data |
| RST | External reset, low active |
| BUSY | Busy status output pin (indicating busy) |
| PWR | Power on/off control. High for on. |

https://www.waveshare.com/product/displays/e-paper/driver-boards/e-paper-driver-hat.htm
https://www.waveshare.com/wiki/E-Paper_Driver_HAT

MEN HVA fuck er PWR?

# TODO Note on Resistor (Display Config)

For the 

<details>
<summary><b>GPIO Configuration for X</b></summary>

| PIN | ESP32 | Description |
| --- | --- | --- |
| VCC | 3V3 | Power positive (3.3V power supply input) |
| GND | GND | Ground |
| DIN | | SPI's MOSI, data input |
| SCLK | | SPI's CLK, clock signal input |
| CS | | Chip selection, low active |
| DC | | Data/Command, low for command, high for data |
| RST | | Reset, low active |
| BUSY | | Busy status output pin (indicating busy) |

</details>

<details>
<summary><b>GPIO Configuration for Y</b></summary>

| PIN | ESP32 | Description |
| --- | --- | --- |
| VCC | 3V3 | Power positive (3.3V power supply input) |
| GND | GND | Ground |
| DIN | | SPI's MOSI, data input |
| SCLK | | SPI's CLK, clock signal input |
| CS | | Chip selection, low active |
| DC | | Data/Command, low for command, high for data |
| RST | | Reset, low active |
| BUSY | | Busy status output pin (indicating busy) |

</details>



