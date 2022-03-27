<h1 align="center">Python Raycasting:</h1><br>

<details>
  <summary>Table of Contents: </summary>
  <ol>
    <li>
      <a href="#about">About</a>
      <ul>
      </ul>
    </li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


## About:

<img src = "https://i.imgur.com/liV51d4.png" width = 900 height = 700>

This is a Python Raycasting Engine, made in pure Python. The engine is able to handle a lot of tasks including: 

* Displaying textures and sprites (the sprite system supports different angles).
* Rendering maps with different sizes, the mini-map will adapt to the rendered map size.
* Displaying different animations (idle, death, attack...
and so on).
* Playing sounds and music.
* Displaying Interactive Buttons.
* Displaying a User Interface (Health, Ammunition and other stuff).
* Player Movement (Keyboard & Mouse).
* Collision (Not the best collision system that you can find).
* And a few more minor features...

The engine is well optimized, relying on the Numba Python Compiler to translate Raycasting functions to machine code.


## Installation:

To be able to run the Python Raycasting Engine you need to have a few Python libraries installed on your computer.

<b>NOTE:</b> Messing with directories may cause some unforeseen consequences...

1. Clone the repository: 

   ```sh
   git clone https://github.com/Carbon32/py-raycasting.git
   ```
2. Install all necessary libraries:

    ```sh
    pip install pygame
    pip install numba
    ```

## License:

Distributed under the MIT License. See `LICENSE` for more information.

