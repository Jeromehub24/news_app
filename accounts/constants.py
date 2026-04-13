"""Role constants used throughout the News App permission system."""

class Roles:
    """Canonical role values and human-readable role choices."""

    READER = "reader"
    EDITOR = "editor"
    JOURNALIST = "journalist"

    CHOICES = [
        (READER, "Reader"),
        (EDITOR, "Editor"),
        (JOURNALIST, "Journalist"),
    ]


ROLE_TO_GROUP = {
    Roles.READER: "Reader",
    Roles.EDITOR: "Editor",
    Roles.JOURNALIST: "Journalist",
}
