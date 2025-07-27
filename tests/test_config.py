from pathlib import Path

from  members_files.config import read_config


def test_config_no_directory(mocker):
    mocker.patch(
        'members_files.config.CONFIG_PATH',
        Path(
            Path(__file__).parent,
            'test_data',
            'not a directory',
            'config.toml')
        )

    config = read_config()
    assert config.xxx == ''


def test_config_save(mocker):
    mocker.patch(
        'members_files.config.CONFIG_PATH',
        Path(Path(__file__).parent, 'test_data', 'config', 'config.toml')
        )

    config = read_config()
    if config.path.is_file():
        config.path.unlink()

    config = read_config()
    config.update('xxx', 6)
    config.save()

    config = read_config()

    assert config.xxx == 6
