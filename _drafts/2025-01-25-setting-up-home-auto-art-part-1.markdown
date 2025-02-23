---
layout: post
title: "Setup automatic art, part 1"
date: 2025-01-25 18:09:47 +0100
categories: homeassistant ai art esp32 raspberry pi
published: false
---


{% highlight python %}
from art import stablediffusion 3
{% endhighlight %}

and setup esp32

{% highlight yaml %}
esphome:
    name: "hello"
{% endhighlight %}

and this is how to solder

| Column1 | Column2 | Column3 |
| ------------- | -------------- | -------------- |
| Item1 | Item1 | Item1 |

You will need to do a long configuration 


From 


<details>
<summary><b>ESPHome configuration</b></summary>

{% highlight yaml %}

esphome:
  name: prettyprettyesp
  platformio_options:
    build_flags: "-DBOARD_HAS_PSRAM"

esp32:
  board: esp32dev # dfrobot_firebeetle2_esp32e
  framework:
    type: arduino
    version: latest

logger:
  level: VERY_VERBOSE

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  on_connect:
    - logger.log: "Connected to wifi"
    - component.update: my_image

http_request:
  id: fetch_image_request
  timeout: 5s
  useragent: esphome/example_device
  verify_ssl: false

online_image:
  - url: http://192.168.1.24:8080/queue.png
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
  clk_pin: GPIO18
  mosi_pin: GPIO23

display:
  - platform: waveshare_epaper
    id: my_display

    cs_pin: 21
    dc_pin: 13
    busy_pin: 34
    reset_pin: 14
    model: 13.3in-k

    reset_duration: 200ms
    update_interval: never
    lambda: |-
      it.image(0, 0, id(my_image), Color::BLACK, Color::WHITE);
      ESP_LOGD("display", "Image displayed successfully");
{% endhighlight %}

</details>


```plantuml!
Bob -> Alice : hello world
```

