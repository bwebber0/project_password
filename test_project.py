from project import (
    opts_input,
    get_chars,
    password_strength,
    password_validate,
    generate_password,
    contains_words,
)
import pytest

all_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!()-.?[]_`~;:@#$%^&*+="


def test_opts_input():
    assert opts_input(["-l", "-n", "-f", "8"]) == (True, False, True, "", True, 8)
    assert opts_input(["-f", "-s", "12"]) == (False, False, False, "all", True, 12)
    assert opts_input(["-u", "-s", "!@&^*#", "12"]) == (False, True, False, "!@&^*#", False, 12)


def test_password_strength():
    assert password_strength("paSsw0rd", all_chars) == (2419740841771008, "MODERATE", {"pass"})
    assert password_strength("2023", "0123456789") == (10000, "WEAK", set())


def test_get_chars():
    assert get_chars(False, False, False, False) == str()
    assert get_chars() == all_chars


def test_password_validate():
    assert password_validate("paSsw0rd", True, True, True, False) == True
    assert password_validate("paSsw0rd", True, True, True, True) == False
    assert password_validate("p@Ssw0rd", True, True, True, True) == True


# A little harder to test the random return value, but some general properties:
def test_generate_password():
    assert len(generate_password(all_chars, 12)) == 12
    assert generate_password(all_chars, 10)[0] != ("." or "-")
    assert (generate_password("0123456789", 10).isdigit() == True)


def test_contains_words():
    assert contains_words("jdpassdmtherekl") == {"pass", "there", "here"}
    assert contains_words("jdpPaSsdmtHerEl") == {"pass", "there", "here"}


def test_sys_exits():
    with pytest.raises(SystemExit):
        opts_input(["-h"])
        opts_input(["--version"])
        opts_input(["-s", "13", "12"])
        opts_input(["13", "12"])
        opts_input(["-j", "12"])