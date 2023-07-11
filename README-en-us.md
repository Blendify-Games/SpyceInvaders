# Spyce Invaders <img src=./res/img/icon.png height="27" width="35"> (veja em [pt-br](./README.md))

This is an open source and *libre* game made by a Space Invaders fan as a tribute and also as an experimentation
targeting the library [pygame-ce](https://pyga.me/) usage. The distribution of this game and its content is free of charge.

## Running this game

This game was developed using python 3.11. After the python installation, it is recomended that you create
an execution virtual environment for the libraries used by this project. Use virtualenv for this.
Install virtualenv package using pip an then create a virtual environment. With an access to a terminal just type:

```bash
> pip install virtualenv     # virtualenv installation
> virtualenv .venv           # virtual environment creation
#------ Alternatively
> pip3 install virtualenv    # use pip3 when python2 and python3 are both available in the system
> python3 -m venv .venv      # virtual environment creation
```

### Steps for configuration and execution:

After the first execution if you want to run the game again just repeat steps 1 and 3.

1. Activate the virtual environment

    ```bash
    # On windows
    > .\.venv\Scripts\activate
    
    # On GNU/Linux or other unix-like systems
    $ source ./.venv/bin/activate
    ```

    * Notice that by activating the virtual environment something like `(.venv)` appears at the beginning of the
      command line on terminal. This indicates that the virtual environment is activated. To deactivate, type `deactivate`
      
2. If this is your first time running the game in this virtual environment, then you should install the game dependencies:

    ```bash
    > pip install -r requirements.txt
    ```

3. Running the game:

    ```bash
    > python main.py
    ```
