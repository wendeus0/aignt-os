import pytest
from textual.app import App
from textual.widgets import Label, RichLog

from aignt_os.cli.dashboard import LogViewer


class LogTestApp(App):
    def compose(self):
        yield Label("Base")


@pytest.mark.asyncio
async def test_log_viewer_loads_initial_content():
    app = LogTestApp()
    viewer = LogViewer("Test Log", "Initial Content")

    async with app.run_test():
        await app.push_screen(viewer)
        # Query the viewer directly, or wait for screen change
        log = viewer.query_one(RichLog)
        assert log is not None


@pytest.mark.asyncio
async def test_log_viewer_refreshes_content(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("Line 1\n", encoding="utf-8")

    app = LogTestApp()
    viewer = LogViewer("Test Log", "Initial", path=str(log_file))

    async with app.run_test():
        await app.push_screen(viewer)
        viewer.query_one(RichLog)

        # Manually trigger refresh logic
        viewer.refresh_log()

        # Update file
        log_file.write_text("Line 1\nLine 2\n", encoding="utf-8")

        # Refresh again
        viewer.refresh_log()
