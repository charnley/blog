---
layout: post
title:  "Building Your Own AI & E-Ink Powered Art Gallery: A Local DIY Guide"
date:   2025-03-02
categories: AI art e-ink esp32 home-assistant
author: Jimmy & Peter
---

TODO Insert gallery photo

![Showing the transition of E-ink screen](../assets/images/eink_art/video/output2.gif)

We built an **e-ink picture frame** using an **ESP32** microprocessor that shows a new daily piece of artwork created by a **local AI diffusion model**.
Each day brings a random and unique image to enjoy. Everything runs on our local network, keeping everything private and off the cloud. It’s simple to have dynamic, AI-generated art on your walls without compromising privacy. Plus, the whole setup fits into our Home Assistant smart home system, which handles the image server and keeps track of the ESP32s.

TODO Better front + back photos

| ![E-ink with AI art ESP32 home assistant based](../assets/images/eink_art/P_20250312_180421_filter.jpg) | ![Backside of E-ink frame with ESP32 and battery](../assets/images/eink_art/P_20250312_180651_filter.jpg) |

**Figure:** Backside of the photoframe, showing the ESP32, E-ink hat and Battery. Include a 1EUR and 2EUR for size reference.

Want to build your own? Here’s how.
If you’re aiming for wireless picture frames, the ESP32 chip is the way to go, though it does require some soldering.
If you’d rather avoid the soldering, you can always use a Raspberry Pi Zero, leaving you with a cable coming out of your frame.

In some areas, we go all in (like with dithering algorithms), while in others, we take shortcuts (like writing yaml instead of C-code).
After all, [we need to finish our projects](https://www.youtube.com/watch?v=4jgTCayWlwc).

## Hardware Requirements

Here’s what you’ll need:

- A computer with a **decent graphics card** to generate AI images
- An **E-ink screen** and an E-ink screen HAT
- For wireless or battery-powered setups: an **ESP32 chip** and a LiPo battery
- For wired setups or if you don’t want to solder: a **Raspberry Pi Zero**
- Optionally, a **Raspberry Pi 5** to host an image server

And you should be comfortable with:

- Python programming
- Basic Linux (shell) commands
- Soldering

While a Raspberry Pi Zero is the best choice for the picture frame due to its size, any Raspberry Pi model will work just fine.
Specifiably, the items we got were;

| Item | Product Link | Price |
| --- | --- | --- |
| DFRobot FireBeetle2 ESP32S3 N16R8 8MB PSRAM [wiki](https://wiki.dfrobot.com/SKU_DFR0975_FireBeetle_2_Board_ESP32_S3) | [https://www.dfrobot.com/product-2676.html](https://www.dfrobot.com/product-2676.html)| ~ 20 EUR |
| DFRobot FireBettle2 ESP32-E N16R2 2M PSRAM  [wiki](https://wiki.dfrobot.com/_SKU_DFR1139_FireBeetle_2_ESP32_E_N16R2_IoT_Microcontroller) | [https://www.dfrobot.com/product-2837.html](https://www.dfrobot.com/product-2837.html) | ~ 15 EUR |
| 1500-5000 mAh LiPo Battery with JST PH 2 Pin connector | | ~ 7 EUR |
| Raspberry Pi 5 | [https://www.raspberrypi.com/products/raspberry-pi-5/](https://www.raspberrypi.com/products/raspberry-pi-5/) | ~120 EUR |
| Raspberry Pi Zero | [https://www.raspberrypi.com/products/raspberry-pi-zero/](https://www.raspberrypi.com/products/raspberry-pi-zero/) | ~12 EUR |
| Waveshare E-ink 13.3" K, with HAT | [https://www.waveshare.com/13.3inch-e-paper-hat-k.htm](https://www.waveshare.com/13.3inch-e-paper-hat-k.htm) | ~150 EUR |

The estimated total cost per frame is around 180 EUR, plus the cost of the physical frame, with the e-ink display being the most expensive component.

We chose ESP32 after browsing this list of compatible devices on PlatformIO.
[registry.platformio.org/platforms/platformio/espressif32/boards?version=5.3.0](https://registry.platformio.org/platforms/platformio/espressif32/boards?version=5.3.0).
The version is locked to 5.3.0 because, at the time of writing, ESPHome uses `platformio=5.3.0`.
The key requirement is that the ESP32 needs PSRAM to download the PNG image over Wi-Fi.

We recommend avoiding Amazon when shopping for components.
If you're based in Switzerland, check out [bastelgarage.ch](https://www.bastelgarage.ch).
Otherwise, a small local shop in your country will likely carry most of the parts.
Unfortunately, we couldn’t find a supplier for the Waveshare 13.3" black/white e-ink display ([Waveshare 13.3" black/white e-ink display](https://amzn.to/4im9Wjj)), so we ordered it from Amazon.

## Software/Service Overview

To keep everything organized and make the workflow easy to manage, we divided the tasks into three main sections: generating images, storing images, and displaying images.
We use our desktop computer with a graphics card to generate images on the fly or through a scheduled job.
We both created different versions of the workflow. You can check out Jimmy’s version at [github.com/charnley/eink-art-gallery](https://github.com/charnley/eink-art-gallery) and Peter’s at [github.com/pgericson/eink-hub](https://github.com/pgericson/eink-hub).


```mermaid
graph LR

    subgraph Desktop [Desktop Computer]
    direction RL
    gpucron@{ shape: rounded, label: "Cron job" }
    GPU@{ shape: rounded, label: "GPU" }
    gpucron --> GPU
    end

    subgraph HA [Home Assistant]
    database@{ shape: db, label: "Image\n.sqlite" }
    canvasserver@{ shape: rounded, label: "Picture\nServer" }
    canvasserver --> database
    end

    subgraph pictures [Picture Frames]

        subgraph esp32 [ESP32]
            esp32eink@{ shape: rounded, label: "E-Ink\nDisplay" }
        end
        subgraph rpi [Rasperry Pi]
            esp32pi@{ shape: rounded, label: "E-Ink\nDisplay" }
        end

    end

    canvasserver -- "POST image" --> rpi
    esp32 -- GET image --> canvasserver

    gpucron -- "GET status" --> canvasserver
    gpucron -- POST image(s) --> canvasserver
   
    classDef default stroke-width:2px;
    classDef default fill: transparent;
    classDef ParentGraph fill: transparent, stroke-width:2px;
    class pictures,HA,Desktop,esp32,rpi ParentGraph
```

The workflow works like this:

- The **picture server** holds a list of AI prompts, each with its associated images, stored in a SQLite database. For our setup, this is hosted on Home Assistant, but it could easily run on any Docker hosting service.
- Every night, the **desktop computer** checks the picture server for prompts that need images. For all of those prompts, the desktop computer generates new images and sends them to the server.
- The **ESP32-powered picture frame(s)** follow a sleep schedule, staying off for 24 hours and waking up at 4 am. When it wakes up, it requests a picture, displays it, and then goes back to sleep.
- The **Raspberry Pi-powered picture frame(s)** host an API for displaying images, so you can send live notifications or images directly to the frame.

The services work seamlessly together and can be easily customized to fit personal needs.
Good separation of concern makes it easier to debug.


## Why and what E-ink?

There are two main reasons we chose e-ink: it looks like a drawing and consumes very little power. But beyond that, it just looks amazing—and I’ve yet to meet anyone who realizes it's screen technology without an explanation. And honestly, I’m always happy to provide that explanation.

What makes it look so realistic is that it’s using ink. You'll know exactly what I mean if you’ve ever used a Kindle or a Remarkable Tablet. The screen comprises tiny "pixels" filled with oil and pigments. The pigments are moved up or down using an electromagnet, which determines the color of each pixel.

Want to learn more? Check out this Wikipedia page on E-Ink [wikipedia.org/wiki/E_Ink](https://en.wikipedia.org/wiki/E_Ink) and this one on electronic paper [wikipedia.org/wiki/Electronic_paper](https://en.wikipedia.org/wiki/Electronic_paper).

Several providers are out there, but the E-ink supplier we’ve gone with is Waveshare. We chose them because others have had good experiences with their products, they offer solid documentation, and their prices are reasonable. In particular, we found the 13.3-inch black-and-white screen to be the perfect fit for our needs, especially when you consider the price versus size. You can check it out here
[waveshare.com/13.3inch-e-paper-hat-k.htm](https://www.waveshare.com/13.3inch-e-paper-hat-k.htm).

The prices can rise quickly as the screen size increases, but we didn’t want to go with the standard 7.5-inch screen—it would look way too small on the wall. We preferred to compromise and go with a larger, though lower-resolution, black-and-white screen. Even with its lower resolution, the 13.3-inch screen fits perfectly and blends seamlessly into our living room.

The screen operates via GPIO pins and binary commands. For the Raspberry Pi, it's pretty much plug-and-play. For the ESP32, however, you'll need to solder each pin and set up the GPIO configuration.

| PIN | Description |
| --- | --- |
| VCC | Power positive (3.3V power supply input) |
| GND | Ground |
| DIN | SPI's MOSI, data input |
| SCLK | SPI's CLK, clock signal input |
| CS | Chip selection, low active |
| DC | Data/Command, low for command, high for data |
| RST | Reset, low active |
| BUSY | Busy status output pin (indicating busy) |
| PWR | Power on/off control |

For the soldering configuration, you can choose which pins go where, but of course, VCC and GND are fixed. The PWR pin is a recent addition to the HAT and controls the power for the E-ink screen. The easiest way to configure this is by soldering it directly to a 3.3 V endpoint on the ESP32.

Another reason we chose this brand of e-ink display is that ESPHome drivers are available, making it much quicker to get everything up and running. Plus, plenty of examples are out there to help you get started. Mind you, most of these examples are for the 7.5-inch model.

> **NOTE:** We also explored the Black-White-Red E-ink display from Waveshare ([13.3" E-Paper HAT-B](https://www.waveshare.com/13.3inch-e-paper-hat-b.htm)), but it required more effort to get it working with ESPHome. Additionally, it takes about 30 seconds to switch pictures, compared to just 3 seconds with the black-and-white version.

## Hosting an AI art model

To fill the local image library we created a Python environment on our desktop computer with access to a graphicscard/GPU.
To have a super powerfull graphics card is not so important, unless you want live prompts.
For a nightly cronjob, it doesn't matter that image generation takes 20 mins or more.

### Selecting an AI model

You can really choose whatever you want here.
We iterated through many models, always trying out the newest during 2024, but in the end for this project, it didn't really matter.
In the end we selected
[Stable Diffusion 3.5](https://stability.ai/news/introducing-stable-diffusion-3-5),
because of easy of setup and what our hardware could handle.
For 1080p graphicscard, it takes about 15mins per image, and with a 4090 it takes ... 3s.
We used Huggingface to setup the model, which requires you to register to get access to the model.

### Note on prompts

For prompts, there are som lessons learned. The biggest lesson is, if you want the art to look nice on the black/white e-ink screen,
you need to use styles that fit that format. E.i. high contrast, grey-scaled and preferably prompt with a e-ink friendly style.

For example, when prompting for a 
"adventurous scifi structure, forest, swiss alps"
the diffusion model will most likely default to a picture/realistic style, which does not translate well to e-ink.
You will need to add something like "pencil sketch" or "ink droplet style" to the prompt to guide the style towards something that looks 
nice on the screen.
Anything drawing, painting, sketch related usually translates well

![Prompt results](../assets/images/eink_art/prompt_example.png)
**Figure:** Showing the results of prompting "scifi building in swiss aps", without (A) and with (B) e-ink friendly keywords, and the results after dithering.

For inspiration, there are many style libraries that has been created. We found that [midlibrary.io](https://midlibrary.io/) gave a quite good selection of style and artists that works well.
Especially the black and white section.

### Hosting image generator service on windows

Since you are following this setup guide, I assume you have a graphics card, and then I will also assume that you are using it on a windows machine.
The most easy way to setup a service is to setup Windows Subsystem Linux.

There was some problems with speed with Windows10 and WSL2, as the read/write to desk was very slow.
Using Windows11 with WSL2 seems way more stable. And note that you need more space than you think to have a Linux subsystem.
However, my experience is with Win11 and WSL2, getting CUDA access to to your windows GPU from linux, is quite smooth.
Setup guide is as following

<details markdown="1">
<summary><b>Setup Linux subsystem linux with CUDA</b></summary>

- Install cuda on windows (probably you already have that) [developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)
- Install wsl [learn.microsoft.com/en-us/windows/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install)

Open a terminal and install wsl

    wsl --install

When WSL is installed, update and setup linux

    # update apt
    sudo apt update
    sudo apt upgrade

Download CUDA bridge from Select Linux, x86, WSL-Ubuntu, 2.0, deb (network)
[developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_network)
as of writing this means
Which means today running the following commands in WSL Ubuntu

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt -y install cuda-toolkit-12-3
```

and lastly setup python, either with `conda`, `uv` or `pip`.

> **NOTE:** WSL will shutdown if no shell is running, so you need to leave a terminal open on your machine.

</details>

And with that you should be able to use a Python environment with CUDA in a linux environment, hosted by Windows.

With the linux subsystem we can setup a job for our service to run every 4am. 
Setup a cronjob with `crontab -e` with the following syntax

```crontab
30 4 * * * cd ~/path/to/project && start-service
```

## Dithering, from a grey-scale photo to binary-black/white

When translating a photo from grey-scale to black-white (meaning binary here), we need to account for the error when we cannot represent grey.
This is called [error diffusion/dithering](https://en.wikipedia.org/wiki/Dither) and is a well known issue.
The default dithering algorithm on most systems is [Floyd-Steinberg dithering](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering),
which is the most numerical accucate way of doing it.
It works by splitting the error associated with going from grey to either black or white into the neighboring pixels, moving from top left.
So if $$*$$ is the current pixel, the error would be distributed like this;

$$
\begin{bmatrix}
         &                                          & *                                        & \frac{\displaystyle 7}{\displaystyle 16} & \ldots \\
  \ldots & \frac{\displaystyle 3}{\displaystyle 16} & \frac{\displaystyle 5}{\displaystyle 16} & \frac{\displaystyle 1}{\displaystyle 16} & \ldots \\
\end{bmatrix}
$$

However, in practice, the numerically correct method dithers the error very densely, making the picture look greyish.
This is especially prominent in our low-resolution images/displays.

With experience we found that the algorithm used in old Macs, [Atkinson Dithering](https://en.wikipedia.org/wiki/Atkinson_dithering),
works really well for low resolution photos.
The difference being that instead of diffusing the full error, only partial will be diffused.

$$
\begin{bmatrix}
  &  & *  & \frac{\displaystyle 1}{\displaystyle 8} & \frac{\displaystyle 1}{\displaystyle 8} \\
  \ldots & \frac{\displaystyle 1}{\displaystyle 8} & \frac{\displaystyle 1}{\displaystyle 8} & \frac{\displaystyle 1}{\displaystyle 8} & \ldots \\
  \ldots &  & \frac{\displaystyle 1}{\displaystyle 8} &  & \ldots \\
\end{bmatrix}
$$

The result is that the image will have more concentrated pixel areas and have a higher contrast. As seen by the following comparison.

![Dithering results](../assets/images/eink_art/dithering_example.png)
**Figure:** A greyscale image (A), dithering using Floyd-Steinberg (B) and using Atkinson Dithering (C).

It might be a little difficult to see, but notice how (B) is more greay than (C).
This is a lot more visually clear when applied on an actual physical low-res e-ink screen.

Now the implementation is doing a lot of for-loops, so Python is not really the best option.
And Pillow only implemented Floyd-Steinberg. 
But using Numba we can get something working really quick.

<details markdown="1">
<summary><b>Atkinson Dithering Python Implementations</b></summary>

```python
import numpy as np
from numba import jit
from PIL import Image

def atkinson_dither(image: Image.Image) -> Image.Image:
    img = np.array(image.convert("L"), dtype=np.int32)
    set_atkinson_dither_array(img)
    return Image.fromarray(np.uint8(img))

@jit
def set_atkinson_dither_array(img: np.ndarray):
    """changes img array with atkinson dithering"""

    low = 0
    heigh = 255

    frac = 8  # Atkinson constant
    neighbours = np.array([[1, 0], [2, 0], [-1, 1], [0, 1], [1, 1], [0, 2]])
    threshold = np.zeros(256, dtype=np.int32)
    threshold[128:] = 255
    height, width = img.shape
    for y in range(height):
        for x in range(width):
            old = img[y, x]
            old = np.min(np.array([old, 255]))
            new = threshold[old]
            err = (old - new) // frac
            img[y, x] = new
            for dx, dy in neighbours:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    # Make sure that img set is between 0 and 255 (negative error could surpass the value)
                    img_yx = img[ny, nx] + err
                    img_yx = np.minimum(heigh, np.maximum(img_yx, low))
                    img[ny, nx] = img_yx
```

</details>

If you are doing multiple colors you can diffuse the error per color channel.

## Displaying the image

For displaying the image on the e-ink, we have two options. Push, with powercable, or pull with battery.

Personally, the iteration was done with a Raspberry Pi, but given that required a USB power cable it removed the immersion as a photoframe.
Note that a white USB cable was used and only one person ever noticed it. However, we knew it was there, and that was enough.
But if you want live updates, like a notification, this is the option you want.

The second option is to use an ESP32 microprocessor, which can be battery-powered. No visible cords.

### Setting up Raspberry Pi API frame

For the Raspberry Pi, the simplest setup would be to setup a FastAPI Python client to receive request and display them.
We use an [Raspberry Pi Zero](https://www.raspberrypi.com/products/raspberry-pi-zero/) because of the small form-factor, to be hidden behind the frame.
Waveshare provides quite good example codes for Python (And other implementations), and is easily the fastest way to get something shown on your screen.
[github.com/waveshareteam/e-Paper](https://github.com/waveshareteam/e-Paper). 

For the Raspberry Pi, [install Debian OS](https://www.raspberrypi.com/documentation/computers/getting-started.html) and `ssh` into the it. 

<details markdown="1">
<summary><b>Setting up Raspberry Pi</b></summary>

```bash
# Enable SPI
# Choose Interfacing Options -> SPI -> Yes
sudo raspi-config
sudo reboot

# Setup Python and dependencies
sudo apt install python3-pip python3-setuptools python3-venv python3-wheel libopenjp2-7

# Create a python env
python3 -m venv project_name

# Activate python env
source ./project_name/bin/activate

# Install the main dependencies with the activated env, but really, use a git repo for this
pip install pillow numpy RPi.GPIO spidev gpiozero spidev
```
</details>

If you have a problem creating a `venv`, because of missing pip, you can;

    python3 -m venv --without-pip project_name
    source env/bin/activate
    wget bootstrap.pypa.io/get-pip.py
    python get-pip.py

With this setup, it should be pretty straightforward to set up a FastAPI solution.
For inspiration, refer to Jimmy's github solution [github.com/charnley/eink_art_gallery](https://github.com/charnley/eink_art_gallery).

Note, because you need to start the API every time the Raspberry Pi is booted, it is worth setting up a `crontab -e` to start you service at boot

    @reboot /path/to/your_script.sh


### Setting up ESPHome and ESP32 frame

Why didn't we write it in C?
Because A) the project needs to end at some point, and B) we both use Home Assistant, it made sense to get all the free stuff out of the box with ESPHome.
[Choose your battles](https://www.youtube.com/watch?v=4jgTCayWlwc) and finish your projects.
ESPHome is a `yaml`-based configuration that creates the binaries to actually flash your devices.
So for the devices you don't write code, but you set it up using modules in yaml format.
Like lego for your ESP32-devices.

The ESPHome eco-system has drivers for most of the WaveShare E-ink displays, but it seems for the 13.3 black-white display we wanted to use, it was not yet implemented.
So Peter wrote the drivers to support this, as seen in [https://github.com/esphome/esphome/pull/6443](https://github.com/esphome/esphome/pull/6443)

For device choice, there are many, many, many options for ESP32s.
Firstly, we tried the example [ESP32 development board](https://www.waveshare.com/e-paper-esp32-driver-board.htm) from Waveshare, which, of course, can display pictures. However, it was not possible to download images over the Internet with the standard ESPHome libraries. 
Because this requires that the ESP32 has [PSRAM](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/external-ram.html).
We iterated through a couple and found that the FireBettle2 ESP32-E and FireBettle2 ESP32S have PSRAM and are well-documented by the producer.

To connect the ESP32 to the E-Paper Driver HAT, select which GPIO pins are connected to each pin defined for the Waveshare HAT (table above).
So, solder solder. Remember your flux.
Example configuration for the FireBettle 2 ESP32-E GPIO to Waveshare HAT GPIO soldering is seen in the table;

| WS HAT PIN  | ESP32-E PIN | Description |
| ---  | ---     |--- |
| PWR  | 3v3     | Power on/off control |
| BUSY | 4/D12   | Busy status output pin (indicating busy) |
| RST  | 14/D6   | Reset, low active |
| DC   | 13/D7   | Data/Command, low for command, high for data |
| CS   | 15/A4   | Chip selection, low active |
| CLK  | 18/SCK  | SPI's CLK, clock signal input |
| DIN  | 23/MOSI | SPI's MOSI, data input |
| GND  | gnd     | Ground |
| VCC  | 3v3     | Power positive (3.3V power supply input) |

The configuration that worked for us for the two FireBettles were (as defined by the ESPHome substitutions in the yaml). Note that the GPIO pin's have multiple names, and to find out which physical ESP32 GPIO is named you will have to read the documentation of the manufactor. In this case FireBettle provides good wiki's to read up on.

The below example assumes that you've setup a addOn/docker service in HomeAssistant, however, the url can be anything on your local network. As long as the payload is a PNG image with the correct resolution. For the 13.3 K model, this is 680x920 pixels.

<details markdown="1">
<summary><b>GPIO Configuration for FireBettle2 ESP32-E</b></summary>

```yaml
substitutions:
  device_id: "example_e"
  wifi_ssid: !secret wifi_ssid
  wifi_password: !secret wifi_password
  wake_up_time: "04:00:00"
  image_url: "http://homeassistant.local:8090/displays/queue.png"

  busy_pin: "GPIO04" # 4/D12
  reset_pin: "GPIO14" # 14/D6
  dc_pin: "GPIO13" # 13/D7
  cs_pin: "GPIO15" # 15/A4
  clk_pin: "GPIO18" #  18/SCK
  mosi_pin: "GPIO23" # 23/MOSI

  waveshare_model: "13.3in-k" # or another waveshare model

esp32:
  board: esp32dev # dfrobot_firebeetle2_esp32e
  framework:
    type: arduino
    version: recommended

esphome:
  name: eink-frame-${device_id}
  friendly_name: "eink frame ${device_id}"
  platformio_options:
    build_flags: "-DBOARD_HAS_PSRAM"
```

</details>

<details markdown="1">
<summary><b>GPIO Configuration for FireBettle2 ESP3S3</b></summary>

```yaml
substitutions:
  device_id: "example_s"
  wifi_ssid: !secret wifi_ssid
  wifi_password: !secret wifi_password
  wake_up_time: "04:00:00"
  image_url: "http://homeassistant.local:8090/displays/queue.png"

  clk_pin: "GPIO12"
  mosi_pin: "GPIO11"
  cs_pin: "GPIO10"
  dc_pin: "GPIO9"
  busy_pin: "GPIO7"
  reset_pin: "GPIO4"

  waveshare_model: "13.3in-k" # or another waveshare model

esp32:
  board: dfrobot_firebeetle2_esp32s3
  framework:
    type: arduino
    version: recommended
```

</details>

After soldering the ESP32 with connectors, we can bring it to life with flashing it using ESPHome.
To setup ESPHome, use a Python environment and install it via `pip`.

```bash
pip install esphome
```

Then setup a `secrets.yaml` with your wifi name and password.

```yaml
wifi_ssid: YourWiFiSSID
wifi_password: YourWiFiPassword
```

Then you flash the ESP with ESPHome using the command;

```bash
esphome run --device /dev/ttyACM0 ./path/to/configuration.yaml
```

Where the device is mounted on either `/dev/ttyACM0` or `/dev/ttyUSB0`, and 0 is in the range 0-2.
You need to define the device argument when flashing a device with a device name; otherwise, ESPHome will try to flash the device over the ethernet using the device name.

With the GPIO soldered and configured, we can try different ESPHome configurations.
Combine the above device-specific substitutions configuration, with the below functionality.
We have made two example configuration that helped us debug along the way.
If you want more examples to get started, visit our github project.

> **NOTE:** The image you are downloading should be in PNG-format (only format supported by ESPHome), and be the exact image size, which in our case is 680x960.

A simple configuration for, connecting to wifi, download a image and displaying it, goes to sleep for 24h, will look like the following `yaml`.
Note the variables below are defined as substitutions above.

```yaml
http_request:
  id: fetch_image_request
  timeout: 5s
  useragent: esphome/example_device
  verify_ssl: false

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  on_connect:
    - component.update: my_image

logger:
  baud_rate: 115200
  level: VERY_VERBOSE

online_image:
  - url: $image_url
    id: my_image
    format: png
    type: BINARY
    on_download_finished:
      then:
        - component.update: my_display
        - logger.log: "Downloaded image"
    on_error:
      then:
        - logger.log: "Error downloading image"

spi:
  clk_pin: $clk_pin
  mosi_pin: $mosi_pin

display:
  - platform: waveshare_epaper
    id: my_display
    cs_pin: $cs_pin
    dc_pin: $dc_pin
    busy_pin: $busy_pin
    reset_pin: $reset_pin
    reset_duration: 200ms
    model: $waveshare_model
    update_interval: never
    lambda: |-
      it.image(0, 0, id(my_image), Color::BLACK, Color::WHITE);
      ESP_LOGD("display", "Image displayed successfully");

deep_sleep:
  run_duration: 40s
  sleep_duration: 25200s # 7h
```

and for a more advanced configuration that

- Wakes up at 4am
- Connectes to wifi
- Tries to download image
- Shows X on image download failure
- Shows image on success
- Sends an estimate of the battery level to Home Assistant

will look like the following `yaml`.

<details markdown="1">
<summary><b>Advanced ESPHome configuration</b></summary>

```yaml
deep_sleep:
  id: deep_sleep_control
  run_duration: 40sec

time:
  - platform: homeassistant
    id: homeassistant_time

logger:
  baud_rate: 115200
  level: DEBUG

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  power_save_mode: light
  on_connect:
    - logger.log: WiFi is connected!
    - logger.log: "Trying to download ${image_url}"
    - component.update: my_image

captive_portal:

online_image:
  - url: $image_url
    id: my_image
    format: png
    type: BINARY
    on_download_finished:
      then:
        - logger.log: "Downloaded image, updating display"
        - display.page.show: page1
        - component.update: my_display
        - delay: 7s
        - deep_sleep.enter:
            id: deep_sleep_control
            until: "${wake_up_time}"
            time_id: homeassistant_time
    on_error:
      then:
        - logger.log: "Error downloading image $(image_url)"
        - display.page.show: page2
        - component.update: my_display
        - delay: 7s
        - deep_sleep.enter:
            id: deep_sleep_control
            until: "${wake_up_time}"
            time_id: homeassistant_time

spi:
  clk_pin: $clk_pin
  mosi_pin: $mosi_pin

display:
  - platform: waveshare_epaper
    id: my_display
    cs_pin: $cs_pin
    dc_pin: $dc_pin
    busy_pin: $busy_pin
    reset_pin: $reset_pin
    reset_duration: 200ms
    model: $waveshare_model
    update_interval: never
    pages:
      - id: page1
        lambda: |-
          it.image(0, 0, id(my_image), Color::BLACK, Color::WHITE);
          ESP_LOGD("display", "Image displayed successfully");
      - id: page2
        lambda: |-
          it.line(0, 0, 50, 50);
          it.line(0, 50, 50, 0);
          ESP_LOGD("display", "Error Image displayed successfully");

api:
   on_client_connected:
     then:
       - sensor.template.publish:
           id: battery_level
           state: !lambda "return id(battery_level).state;"
       - sensor.template.publish:
           id: battery_voltage
           state: !lambda "return id(battery_voltage).state;"

ota:
  - platform: esphome

 sensor:
   - platform: adc
     pin: VDD
     name: "Battery Voltage"
     id: battery_voltage
     update_interval: 60s
     attenuation: auto
     unit_of_measurement: "V"
     accuracy_decimals: 2

   - platform: template
     name: "Battery Level"
     id: battery_level
     unit_of_measurement: "%"
     accuracy_decimals: 0
     lambda: |-
       float voltage = id(battery_voltage).state;
       if (voltage < 3.0) return 0;
       if (voltage > 4.2) return 100;
       return (voltage - 3.0) / (4.2 - 3.0) * 100.0;

binary_sensor:
  - platform: status
    name: "${device_id} Status"
    id: device_status
```
</details>

> **Note:** If your picture gets less visible (greyish), the more complicated the image is, you are using the wrong display-config. [waveshare.com/wiki/E-Paper_Driver_HAT](https://www.waveshare.com/wiki/E-Paper_Driver_HAT).

> **Note:** If your picture does not refresh entirely when changing photos, you might have a loose connection. Re-check your soldering connections.

## Battery choice

Now all there is left for the project is to find a nice battery. The critiera is we didn't want to take the frame down and re-charge too often, and the battery needs to have a slim form-factor so it fits behind the photo frame.

To figure out how much mAh we need in a LiPo battery we need to calculate how much power our project is consuming per-day.
We split it into two consumptions, deep-sleep power consumption and a per-image switch.
For the image switch consumption we bought a USB-C amphere measuring, noteing down the peak for simplicity. A better way would be to setup a Voltmeter between in chain with the battery and the device.
However, we were lazy.

The peak during a picture change we measured to be $$0.128 \text{Ampere}$$.

For the deep-sleep consumption, the usage was so small that we could not measure it with out amphere meter.
However, googling we found the ESP32 has a very efficient deep-sleep of only $$10 \mu \text{Ampere}$$ usage.
Accordding to the [Espressif source](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf).

As a reminder, for the following calculations, Watt is equal to 1 joule per second and 24h is equal to 24h = 86400s.

$$
\begin{align}
     E_\text{Battery} &= \frac{\text{[Battery mAh]} \cdot \text{[Battery Voltage]}}{1000} \cdot 3600 \text{ Joule / Wh}\\
     &= \left (1500 \text{mAh} \cdot 3.3 \text{V} \right ) / 1000 \cdot 3600 \text{J/Wh} = \underline{17820 \text{ Joule}}\\
    E_\text{picture change} &= \text{Voltage} \cdot \text{Ampere} \cdot \text{Time}\\
    &= 3.3 \text{V} \cdot 0.128\text{A} \cdot 20\text{sec} = \underline{8.4 \text{ Joule}}\\
    E_\text{daily sleep} &= 3.3 \text{V} \cdot 0.00001 \text{A} \cdot 86400 \text{sec} = \underline{2.85 \text{ Joule}}\\
    \text{Battery Life} &= \frac{E_\text{Battery} }{(E_\text{daily sleep} + N \cdot E_\text{picture change})} \\
                 &= \frac{19980 \text{ J}}{\left (3.2 + 1 \cdot 9.5 \right ) \text{J/day}} \approx 1500 \text{ days} \approx 4 \text{ years}
\end{align}
$$

Where $$N$$ is number of picture changes per day.
In our example it is just once per night.
Which leads us to if only one change per day, the battery should last us 4 years.... which seems unrealistic.
Note that LiPo batteries has a natural de-charge of 1-5% per month [cite needed].

Here is a Python function for the lazy.

<details markdown="1">
<summary><b>battery_lifetime.py</b></summary>

```python
def battery_lifetime(
    battery_mah: int, # mAh
    switch_per_day: int,
    switch_ampere: float = 0.128, # ampere
    switch_time: float = 20, # sec
):
    battery_voltage = 3.3
    sleep_ampere = 0.00001
    daily_seconds = 86400
    e_battery = (battery_mah * battery_voltage)/1000 * 3600
    e_picture_change = battery_voltage * switch_ampere * switch_time
    e_daily_sleep = battery_voltage * sleep_ampere * daily_seconds
    days = (e_battery)/(e_daily_sleep + switch_per_day*e_picture_change)
    return days
```

</details>

> **NOTE:** The battery you buy will most likely not arrive in the correct +/- configuration, or even the correct JST connector size. When switching the cables, *do not* let the +/- ends touch eachother unless you want to order a new battery.

## Mounting on the frame

Mounting the project on the back side of your frame, you have some options.
If you want to go full-overkill, do as Peter, which is create a custom 3D printed mount to be glued on the backside.

TODO Insert Peter picture

Or if you don't have a 3D printer, do as Jimmy, which is to use M2 screws and M2 x5mm spacers, hot glued on the backside. Screw in the screws and spacers on the device, then place them on the backside with hotglue.

![Backside of E-ink frame with ESP32, spacers, and glue]({{site.baseurl}}/assets/images/eink_art/eink_backside_glue_filter.jpg)

Both options will make it possible to screw the devices off for debugging/maintenance.
Others on the internet has been seen to hot-glue the device directly to backside of the frame, which is insane... don't do that.

To make it look proffesional, use a passepartout (the white thing around the display).
They usually come with frames.
However, note that the default 30x40cm passepartout Jimmy could get locally, was just showing the black outline of the screen.
In the end Jimmy has to get a custom cut to fit the display, which was very expensive, but gave the final touch to eleminate all possible signs that it was not a real painting.

## The result

TODO Insert image gallery


## Note on the next version

It was hard to finish, because there is always more to do.
It was to say stop.
For the next version, we wanted to explore

- We want to use `olama` model to generate the prompts for the picture generation, based on themes. For example if we have a Mexican-themed party, all the prompts would be based in Mexican native art.
- ESP32 and ZigBee-based live update, using ZigBee to do a wake-on-demand. Making the ESP32 push-friendly.
- The is a new Waveshare screen [waveshare.com/product/displays/e-paper/epaper-1/13.3inch-e-paper-hat-plus-e.htm](https://www.waveshare.com/product/displays/e-paper/epaper-1/13.3inch-e-paper-hat-plus-e.htm) wich is 13.3 inches, higher resolution and full of colours. This would be a very cool upgrade. Requires some deep-dive into making ESPHome work with another interface.
- Either with a webcam, or with pre-defined pictures, generate picture of the guests who are coming to visit you, similar (github.com/bytedance/InfiniteYou)[(https://github.com/bytedance/InfiniteYou)]
- Have better infographics and integration to local weather. For example knowing when there is new snow, and integrate with Home Assistant to let one know when and where to go ski.

## Thanks

Ananda for providing answers when stuck.
Kristoffer for proof-reading.
Patrick for soldering.
