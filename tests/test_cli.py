from typer.testing import CliRunner
from promptstrike.cli import app

runner = CliRunner()


def test_scan_reports_the_asr_of_every_suite():
    result = runner.invoke(
        app, ["scan", "--target", "local", "--repeats", "1"])
    assert result.exit_code == 0
    assert result.output.count("SUITE ASR") == 3
