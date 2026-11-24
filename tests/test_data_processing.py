from modules.data_processing import split_profile_data


def test_split_profile_data_creates_sectioned_nodes():
    profile = {
        "full_name": "Ada Lovelace",
        "experiences": [{"title": "Mathematician", "company": "Analytical Engine"}],
        "certifications": [],
    }

    nodes = split_profile_data(profile)

    assert len(nodes) == 2
    assert {node.metadata["section"] for node in nodes} == {
        "full_name",
        "experiences",
    }
