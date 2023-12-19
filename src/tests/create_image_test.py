from os.path import exists

from src.main import create_image


def test_create_image(tmpdir):
    """Exercise the `create_image` function and verify that the folders and files were created.  This is a sanity check to ensure that the image was created.

    Args:
        tmpdir (_type_): Pytest tmpdir object.
    """

    # Create the image
    tmpdir = str(tmpdir)
    create_image(tmpdir)

    # Check that folders and files exist
    assert exists(tmpdir + "/com.microsoft.VSCode")
    assert exists(tmpdir + "/com.microsoft.VSCode.ShipIt")
    assert exists(tmpdir + "/Code")
    assert exists(tmpdir + "/com.microsoft.VSCode.savedState")
    assert exists(tmpdir + "/.vscode")
