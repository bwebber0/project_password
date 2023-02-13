import sys
import random
import re
import getopt
import string

from english_words import get_english_words_set

SHORT_USAGE = f"Usage: python project.py [[options] <password_length>]"
USAGE = (
    f"Usage: python project.py [options] <password_length>\n"
    f"       python project.py\n"
    f"  options:\n"
    f"    -h, --help                   Display help.\n"
    f"    -v, --version                Display version.\n"
    f"    -l, --lower                  Include lowercase letters in character set.\n"
    f"    -u, --upper                  Include uppercase letters in character set.\n"
    f"    -n, --number                 Include numbers in character set.\n"
    f"    -s, --special=<spec_chars>   Include special characters. [default: all or !()-.?[]_`~;:@#$%^&*+=]\n"
    f"                                 NOTE: If none of the character types are selected, the default is to use all character types.\n"
    f"    -f, --force                  Force password to contain at least 1 of each of the selected character types.\n"
         )

__version__ = "0.1.0"


def main():
    """Generates and prints a (pseudo-random) passwords, with indication of strength and whether it contains an English word."""
    print("----- PROJECT PASSWORD -----")
    args = sys.argv[1:]
    lower, upper, number, special, force, length = opts_input(args)
    pw_chars = get_chars(lower, upper, number, special)

    while True:
        while True:
            password = generate_password(pw_chars, length)
            perm, strength, words = password_strength(password, pw_chars)
            if force:
                valid = password_validate(password, lower, upper, number, special)
                if valid:
                    break
                else:
                    continue
            else:
                break
        print((14 + length) * "#")
        print(f"\n  PASSWORD: {password}  \n")
        print((14 + length) * "#")
        print(f"This is a {strength} password.")
        print(f"With this password length and character set there are {perm:.3e} possibilities in the space.")
        if words:
            print(f"CAUTION: This password contains dictionary words. {words}")

        if strength == "VERY STRONG":
            break
        else:
            redo = input("Generate another password with different requirements? [y/N] ")
            if redo == ("y" or "Y"):
                print("...\n...\n...")
                lower, upper, number, special, force, length = opts_input([])
                pw_chars = get_chars(lower, upper, number, special)
                continue
            else:
                break


def opts_input(args):
    """
    Returns option flags and arguments by handling command-line arguments or user input.

    Parameters
    ----------
    args : list
        List of command-line argument and options

    Returns
    -------
    lower : bool
        Flag for using lowercase letters.

    upper : bool
        Flag for using uppercase letters.

    number : bool
        Flag for using numbers.

    special : str
        Special characters to be used, or 'all' for all allowed special characters.

    force : bool
        Flag to indicate at least 1 of each character type to be used.

    length: int
        Password length.
    """

    if len(args) > 0: # Command-line arguments/options
        try:
            optlist, arg = getopt.getopt(
            args,
            "vhluns:f",
            ["version", "help", "lower", "upper", "number", "special=", "force"],
            )
        except getopt.GetoptError:
            sys.exit(f"ERROR: An option was not recognised. See available options below.{USAGE}")
        lower = False
        upper = False
        number = False
        special = ""
        force = False

        if len(arg) > 1:
            sys.exit(f"ERROR: There should be only 1 positional argument for password length\n{SHORT_USAGE}")

        chars_specified = False
        for o, a in optlist:
            if o in ("-v", "--version"):
                print(VERSION)
                sys.exit()
            elif o in ("-h", "--help"):
                print(USAGE)
                sys.exit()
            elif o in ("-f", "force"):
                force = True
            elif o in ("-l", "--lower", "-u", "--upper", "-n", "--number", "-s", "--special"):
                chars_specified = True
                if o in ("-l", "--lower"):
                    lower = True
                elif o in ("-u", "--upper"):
                    upper = True
                elif o in ("-n", "--number"):
                    number = True
                elif o in ("-s" "--special"):
                    # Work around ambiguity with option -s taking an argument, when followed by positional argument for the length.
                    if a.isdigit() and not arg:
                        arg.append(a)
                        special = "all"
                    elif a.isalnum() and arg:
                        sys.exit(f"ERROR: Only special characters are expected as argument to -s or --special\n{USAGE}")
                    else:
                        special = a

        if not chars_specified:
            lower = True
            upper = True
            number = True
            special = "all"

        try:
            length = int(arg[0])
        except ValueError:
            sys.exit(f"ERROR: Password length must be of type: int \n{SHORT_USAGE}")
        if 100 < length < 4:
            sys.exit(f"ERROR: Password length must be between 4 and 100. \n{SHORT_USAGE}")

    else:  # With no command-line arguments, program asks user for input
        print("What options would you like for your new password?")
        length = 0
        while length < 4:
            try:
                length = int(
                    input("* Set password character length (between 4 and 100): ")
                )
            except ValueError:
                print("Must be an integer, 4 or greater.")

        low = input("* Contains lowercase letters [Y/n]? ")
        up = input("* Contains uppercase letters [Y/n]? ")
        num = input("* Contains numbers [Y/n] ? ")
        spec = input("* Contains special characters [Y/n or (s)elect]? ")
        if low.lower() == ("n" or "no"):
            lower = False
        else:
            lower = True
        if up.lower() == ("n" or "no"):
            upper = False
        else:
            upper = True
        if num.lower() == ("n" or "no"):
            number = False
        else:
            number = True
        if spec.lower() == ("n" or "no"):
            special = ""
        elif spec.lower() == ("s" or "select"):
            special = input(
                "  - Type which special characters you would like (surrounded by single-quotes ''):  !()-.?[]_`~;:@#$%^&*+=  "
            )
        else:
            special = "!()-.?[]_`~;:@#$%^&*+="

        f = input(
            "* Do you require at least 1 of each selected character type in the password [y/N]? "
        )
        print("...")
        if f.lower() == ("y" or "yes"):
            force = True
        else:
            force = False

    return lower, upper, number, special, force, length


def get_chars(lower=True, upper=True, number=True, spec_chars="all"):
    """Returns a string of characters.

    Based on the following (from IBM):
    Under normal circumstances, a valid user ID and password can contain the following characters:
    - Lowercase characters {a-z}
    - Uppercase characters {A-Z}
    - Numbers {0-9}
    - Special  {!()-.?[]_`~;:@#$%^&*+=}
    * Dash {-} or Period {.} are not supported as the first character in the user ID or password

    Parameters
    ----------
    lower : bool
        Flag for using lowercase letters.

    upper : bool
        Flag for using uppercase letters.

    number : bool
        Flag for using numbers.

    special : str
        Special characters to be used. Alternatively 'all' indicates to use all allowed special characters.

    Returns
    -------
    chars_str : str
        Character string.
    """

    chars_str = str()
    if lower:
        chars_str += string.ascii_lowercase
    if upper:
        chars_str += string.ascii_uppercase
    if number:
        chars_str += string.digits
    if spec_chars:
        allowed = "!()-.?[]_`~;:@#$%^&*+="
        if spec_chars == "all":
            spec_str = allowed
        else:
            spec_str = str()
            for s in spec_chars:
                if s in allowed:
                    spec_str += s
        chars_str += spec_str

    return chars_str


def generate_password(chars, length):
    """Returns a randomly generated password.

    Based on the following (from IBM):
    Under normal circumstances, a valid user ID and password can contain the following characters:
    # Lowercase characters {a-z}
    # Uppercase characters {A-Z}
    # Numbers {0-9}
    # Special  {!()-.?[]_`~;:@#$%^&*+=}
    * Dash {-} or Period {.} are not supported as the first character in the user ID or password

    Parameter
    ---------
    chars : set
        Character set used to generate the password.

    length : int
        Password length.

    Returns
    -------
    password : str
        (Pseudo)-randomly generated password.
    """
    random.seed()

    for n in range(length):
        if n == 0: # remove . and _ from the first character
            _ = chars.replace(".", "")
            first_char = _.replace("_", "")
            password = random.choice(first_char)
        else:
            password += random.choice(chars)

    return password


def password_strength(password, chars):
    """
    Returns password strength, possible permutations and English words used  in password.

    Parameters
    ----------
    password : str
        Password or passphrase.

    chars : str
        Character string used to generate the password.

    Returns
    -------
    perms : int
        Possibility space for given number characters.

    strength: str
        Indicator of password strength.

    words : set
        Set of English words found in the password.
    """

    length = len(password)
    if ("." and "_") in chars:
        perms = (len(chars) - 2) * (len(chars) ** (length - 1))
    elif ("." or "_") in chars:
        perms = (len(chars) - 1) * (len(chars) ** (length - 1))
    else:
        perms = len(chars) ** (length)

    words = contains_words(password)

    if perms < 1e7:
        strength = "WEAK"
    elif 1e6 <= perms < 1e14:
        if words:
            strength = "WEAK"
        else:
            strength = "MODERATE"
    elif 1e14 <= perms < 1e22:
        if words:
            strength = "MODERATE"
        else:
            strength = "STRONG"
    else:
        if words and perms < 1e30:
            strength = "STRONG"
        else:
            strength = "VERY STRONG"

    return perms, strength, words


def password_validate(password, lower, upper, number, special):
    """
    Validates if password contains at least 1 character from each selected character set.

    Parameter
    ---------
    password : str
        Password or passphrase.

    lower : bool
        Flag for using lowercase letters.

    upper : bool
        Flag for using uppercase letters.

    number : bool
        Flag for using numbers.

    special : str
        Characters to be used, or 'all' indicating all allowed special characters.

    Returns
    -------
    bool
        True if 1 of each selected character set is found, False otherwise.
    """
    if lower:
        if not re.search(r"[a-z]", password):
            return False
    if upper:
        if not re.search(r"[A-Z]", password):
            return False
    if number:
        if not re.search(r"[0-9]", password):
            return False
    if special:
        if not re.search(r"[!()\-.?\[\]_`~;:@#$%\^&*+=]", password):
            return False

    return True


def contains_words(text):
    """
    Returns any English words of 4 or more characters contained in text, case-insensitively.

    Parameters
    ----------
    text : str
        Text containing any type of character.

    Returns
    -------
    words : set
        Set of English words found in text.
    """
    min = 4
    len_text = len(text)

    strs_in_text = set()
    for i in range(0, len_text - min):
        for j in range(min, len_text - i):
            x = text[i : i + j].lower()
            strs_in_text.add(x)

    english_words = get_english_words_set(["web2"], lower=True)
    words = set()
    for string in strs_in_text:
        if string in english_words:
            words.add(string)

    return words


if __name__ == "__main__":
    main()