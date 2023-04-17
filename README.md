<div align="center">
  
## Ciphify: Password Management Utility

> This utility provides secure & simple password management utility, that can create pronounceable passwords, store passwords using AES-GCM symmetric encryption, & be easily used via a CLI



<div align="left">
<br>
<br>


### Installation

Current installation involves installing this tool locally using the --user flag with pip (pip install --user package_name). This installs `ciphy` in the user-specific site-packages directory, which helps to avoid conflicts with system packages and allows for easy management of user-specific packages.

#### Clone this repository
```bash
git clone https://github.com/Merlin1A/ciphify.git
```

#### Change to the project directory
```bash
cd ciphify
```

#### Install the package
```bash
pip install --user --editable .
```

<br>

*Please note that is also possible to install this in a virtual environement or container like `venv`, `conda`, `pipenv`, `docker`, etc. At the moment, I have not written installation intructions for those environments, but the changes to make `ciphy` work in those environments should be small.*  

<br>


### Usage

Once installed, `ciphy` should be able to be used from the bash shell directly. 

Test it out by invoking the help flag:

```bash
ciphy -h
```

#### Commands

There are a variety of commands related to password encryption, generation, strength testing, & descryption. All commands are listed below.

- gen_pass 
- encrypt
- decrypt

### License

MIT License

### Disclamer
Disclamer Ciphify is currently in active development, and there likely will be breaking changes. There are no guarantees, either implied or explicit, made by this software or me at this stage.
