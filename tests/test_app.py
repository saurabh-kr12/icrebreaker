def test_chat_requires_loaded_profile():
    from app import chat_with_profile

    history = chat_with_profile(
        None,
        "What is this person's role?",
        [],
        "Career analysis",
    )

    assert history[0]["role"] == "user"
    assert "No profile loaded" in history[1]["content"]
