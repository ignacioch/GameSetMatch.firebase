from gamesetmatch.models.player_info import PlayerInfo

def test_player_info_from_dict():
    player_info_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "profile_picture_url": "http://example.com/johndoe.jpg",
        "date_of_birth": "1990-01-01"
    }
    
    player_info = PlayerInfo.from_dict(player_info_data)
    
    assert player_info.name == "John Doe"
    assert player_info.email == "john.doe@example.com"
    assert player_info.profile_picture_url == "http://example.com/johndoe.jpg"
    assert player_info.date_of_birth == "1990-01-01"

def test_player_info_to_dict():
    player_info = PlayerInfo(
        name="John Doe",
        email="john.doe@example.com",
        profile_picture_url="http://example.com/johndoe.jpg",
        date_of_birth="1990-01-01"
    )
    
    player_info_dict = player_info.to_dict()
    
    assert player_info_dict["name"] == "John Doe"
    assert player_info_dict["email"] == "john.doe@example.com"

def test_player_info_str_repr():
    player_info = PlayerInfo(
        name="John Doe",
        email="john.doe@example.com",
        profile_picture_url="http://example.com/johndoe.jpg",
        date_of_birth="1990-01-01"
    )
    
    assert str(player_info) == "PlayerInfo(name=John Doe, email=john.doe@example.com, profilePictureUrl=http://example.com/johndoe.jpg, dateOfBirth=1990-01-01)"
    assert repr(player_info) == "PlayerInfo(name=John Doe, email=john.doe@example.com, profilePictureUrl=http://example.com/johndoe.jpg, dateOfBirth=1990-01-01)"
