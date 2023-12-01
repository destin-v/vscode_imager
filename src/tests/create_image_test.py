from src.main import create_image
from os.path import exists


def test_create_image(tmpdir):
    # Create the image
    tmpdir = str(tmpdir)
    create_image(tmpdir)

    # Check that folders and files exist
    assert exists(tmpdir + "com.microsoft.VSCode")
    assert exists(tmpdir + "com.microsoft.VSCode.ShipIt")
    assert exists(tmpdir + "Code")
    assert exists(tmpdir + "com.microsoft.VSCode.savedState")
    assert exists(tmpdir + ".vscode")
