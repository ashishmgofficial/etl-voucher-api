from etl.enums import Domain


def test_domain_enum():
    assert Domain.get_registered_domains() == ["customer"]
