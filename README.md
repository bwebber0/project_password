# PROJECT PASSWORD

Project Password is a (pseudo)-random password generator.

### Description
Project Password generates a random password with a length of between 4 and 100 characters. The random number generator used is from the module `random`.

Project Password also gives an indication of password strength, number of password possibilities for the given character space and password length being used, and if the generated password contains any English dictionary words of 4 characters or more.

As default the character set according to [IBM](https://www.ibm.com/docs/en/baw/19.x?topic=security-characters-that-are-valid-user-ids-passwords) is used for generating passwords. These characters are split into subsets of lowercase letters, uppercase letters, numbers and special characters which can optionally be chosen in any combination to form the generating set of characters for the password. Additionally, individual special characters can be specified by the user, to use just a subset of the allowed special characters. There is also the option to include at least 1 of each selected character type in the password.

While longer password using all possible sets of characters are recommended for a secure password, the options to use smaller character sets and shorter passwords gives some flexibilty. This is useful for account passwords where certain characters are not allowed, or for example to generate a short 4-digit PIN number.

### Requirements
Project Password requires the pip-installable package [English-words](https://pypi.org/project/english-words/). This gives a not-so-complete set of English words to compare to sub-strings in the password.

### Installation
Add directory ```/project/project.py``` to the path.

### Usage
Project Password can be run from the command-line with options and a positional argument for the `<password_length>`, or run without arguments the program will prompt for user input.

Additionally, after generating a password that is not "very strong", the user is prompted to generate another password with new requirements. If the user enters "y", the program prompts are given for each option and password length.

#### Command-line
```
Usage: python project.py [options] <password_length>
  options:
    -h, --help                   Display help.
    -v, --version                Display version.
    -l, --lower                  Include lowercase letters in character set.
    -u, --upper                  Include uppercase letters in character set.
    -n, --number                 Include numbers in character set.
    -s, --special=<spec_chars>   Include special characters. [default: all or !()-.?[]_`~;:@#$%^&*+=]
                                 NOTE: If none of the character types are selected, the default is to use all character types.
    -f, --force                  Force password to contain at least 1 of each of the selected character types.
```
##### Command-Line Example
```
project/ $ python project.py -l -s '!@#$%' 10
----- PROJECT PASSWORD-----
########################

  PASSWORD: xl%btcisxd

########################
This is a STRONG password.
With this password length and character set there are 8.196e+14 possibilities in the space.
Generate another password with different requirements? [y/N]
```

#### Interactive
To run in interactively, type:
```
$ python project.py
```

##### Interactive Example
```
$ python project.py
----- PROJECT PASSWORD -----
What options would you like for your new password?
* Set password character length (between 4 and 100): 12
* Contains lowercase letters [Y/n]? y
* Contains uppercase letters [Y/n]? y
* Contains numbers [Y/n] ? y
* Contains special characters [Y/n or (s)elect]? n
* Do you require at least 1 of each selected character type in the password [y/N]? y
...
##########################

  PASSWORD: rQ(Fz[wg5;MW

##########################
This is a VERY STRONG password.
With this password length and character set there are 1.205e+23 possibilities in the space.
```

#### Video Demo <URL HERE>

[Watch video demo](https://youtu.be/4XrXEO4vksM)


#### License
[MIT License](https://choosealicense.com/licenses/mit/)
