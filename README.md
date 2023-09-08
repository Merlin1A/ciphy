
<div align="center">
  
## Ciphy: Password Management Utility
  
> This utility provides a secure & simple password management utility that can create pronounceable passwords, store passwords using AES-GCM symmetric encryption, and be easily used via a bash CLI.

<div align="left">
<br>
<br>
  
### Installation
The utility provides multiple ways for installation, including a convenient install.sh script and the traditional pip-based method.

#### Using install.sh script
Simply download the install.sh from the repository and run it to automate the installation process.

```bash
wget https://github.com/Merlin1A/ciphy/raw/main/install.sh
chmod +x install.sh
./install.sh
```

#### Manually via pip
If you'd rather install it manually, follow the steps below:

Clone this repository
```bash
git clone https://github.com/Merlin1A/ciphy.git
cd ciphy
pip install --user --editable .
```

<be>

### Usage
Once installed, 'ciphy' should be accessible from the bash shell directly.

Test it out by invoking the help flag:

```bash
ciphy -h
```

#### Commands

ciphy offers a variety of commands related to password encryption, generation, strength testing, and decryption. All commands are designed to work seamlessly through the CLI.

- gen_pass: Generate one or multiple secure passwords based on your configuration. The generated password can be copied to the clipboard or saved to a secure temporary file, among other options.

- encrypt: Encrypt a given text file containing passwords or other sensitive information. It uses AES-GCM encryption, and you can specify whether to overwrite the original file or create a new encrypted file.

- decrypt: Decrypt a previously encrypted file back to its original format. You'll be prompted to input the password used for encryption.

<be>

### License

MIT License

### Disclaimer
*__Disclamer__* _Ciphy is currently in active development, and there likely will be breaking changes. There are no guarantees, either implied or explicit, made by this software or me at this stage._

<be>

### Contact
If you have any questions, suggestions, or general feedback, feel free to reach out. Your input is highly valued.

<br>
</div>
