from gamesetmatch.models.player_info import PlayerInfo, Level
import pytest

@pytest.mark.parametrize("player_info_data, expected_level", [
    ({
        "name": "John Doe",
        "email": "john.doe@example.com",
        "profile_picture_url": "http://example.com/johndoe.jpg",
        "date_of_birth": "1990-01-01",
        "tel_number": "123-456-7890",
        "areas": [10, 20],
        "level": "beginner"
    }, Level.BEGINNER),
    ({
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "profile_picture_url": "http://example.com/janedoe.jpg",
        "date_of_birth": "1991-02-02",
        "tel_number": "987-654-3210",
        "areas": [30, 40],
        "level": Level.INTERMEDIATE
    }, Level.INTERMEDIATE),
])
def test_player_info_from_dict(player_info_data, expected_level):
    player_info = PlayerInfo.from_dict(player_info_data)
    
    assert player_info.name == player_info_data["name"]
    assert player_info.email == player_info_data["email"]
    assert player_info.profile_picture_url == player_info_data["profile_picture_url"]
    assert player_info.date_of_birth == player_info_data["date_of_birth"]
    assert player_info.tel_number == player_info_data["tel_number"]
    assert player_info.areas == player_info_data["areas"]
    assert player_info.level == expected_level


@pytest.mark.parametrize("player_info_data", [
    ({
        "name": "John Doe",
        "email": "john.doe@example.com",
        "profile_picture_url": "http://example.com/johndoe.jpg",
        "date_of_birth": "1990-01-01",
        "tel_number": "123-456-7890",
        "areas": [10, 20],
        "level": "invalid_level"
    }),
    ({
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "profile_picture_url": "http://example.com/janedoe.jpg",
        "date_of_birth": "1991-02-02",
        "tel_number": "987-654-3210",
        "areas": [30, 40],
        "level": 12345
    }),
])
def test_player_info_from_dict_invalid_level(player_info_data):
    with pytest.raises(ValueError, match="Invalid level value"):
        PlayerInfo.from_dict(player_info_data)

def test_player_info_to_dict():
    player_info = PlayerInfo(
        name="John Doe",
        email="john.doe@example.com",
        profile_picture_url="http://example.com/johndoe.jpg",
        date_of_birth="1990-01-01",
        tel_number="123-456-7890",
        areas=[10, 20],
        level=Level.BEGINNER
    )
    
    player_info_dict = player_info.to_dict()
    
    assert player_info_dict["name"] == "John Doe"
    assert player_info_dict["email"] == "john.doe@example.com"
    assert player_info_dict["profile_picture_url"] == "http://example.com/johndoe.jpg"
    assert player_info_dict["date_of_birth"] == "1990-01-01"
    assert player_info_dict["tel_number"] == "123-456-7890"
    assert player_info_dict["areas"] == [10, 20]
    assert player_info_dict["level"] == Level.BEGINNER.value

def test_player_info_str_repr():
    player_info = PlayerInfo(
        name="John Doe",
        email="john.doe@example.com",
        profile_picture_url="http://example.com/johndoe.jpg",
        date_of_birth="1990-01-01",
        tel_number="123-456-7890",
        areas=[10, 20],
        level=Level.BEGINNER
    )
    
    expected_str = ("PlayerInfo(name=John Doe, email=john.doe@example.com, "
                    "profile_picture_url=http://example.com/johndoe.jpg, "
                    "date_of_birth=1990-01-01, tel_number=123-456-7890, areas=[10, 20], level=beginner)")
    expected_repr = ("PlayerInfo(name=John Doe, email=john.doe@example.com, "
                     "profile_picture_url=http://example.com/johndoe.jpg, "
                     "date_of_birth=1990-01-01, tel_number=123-456-7890, areas=[10, 20], level=beginner)")
    
    assert str(player_info) == expected_str
    assert repr(player_info) == expected_repr