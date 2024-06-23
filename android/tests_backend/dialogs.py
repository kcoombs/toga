import asyncio

import pytest


class DialogsMixin:
    def _setup_alert_dialog_result(self, dialog, buttons, selected_index):
        cleanup = dialog._impl.cleanup

        def auto_cleanup(future):
            async def _close_dialog():
                # Inject a small pause without blocking the event loop
                await asyncio.sleep(1.0 if self.app.run_slow else 0.2)
                try:
                    dialog_view = self.get_dialog_view()
                    self.assert_dialog_buttons(dialog_view, buttons)
                    await self.press_dialog_button(dialog_view, buttons[selected_index])
                except Exception as e:
                    # An error occurred closing the dialog; that means the dialog
                    # isn't what as expected, so record that in the future.
                    future.set_exception(e)

            asyncio.ensure_future(_close_dialog())

            return cleanup(future)

        dialog._impl.cleanup = auto_cleanup

    def setup_info_dialog_result(self, dialog):
        self._setup_alert_dialog_result(dialog, ["OK"], 0)

    def setup_question_dialog_result(self, dialog, result):
        self._setup_alert_dialog_result(dialog, ["No", "Yes"], 1 if result else 0)

    def setup_confirm_dialog_result(self, dialog, result):
        self._setup_alert_dialog_result(dialog, ["Cancel", "OK"], 1 if result else 0)

    def setup_error_dialog_result(self, dialog):
        self._setup_alert_dialog_result(dialog, ["OK"], 0)

    def setup_stack_trace_dialog_result(self, dialog, result):
        pytest.skip("Stack Trace dialog not implemented on Android")

    def setup_save_file_dialog_result(self, dialog, result):
        pytest.skip("Save File dialog not implemented on Android")

    def setup_open_file_dialog_result(self, dialog, result, multiple_select):
        pytest.skip("Open File dialog not implemented on Android")

    def setup_select_folder_dialog_result(self, dialog, result, multiple_select):
        pytest.skip("Select Folder dialog not implemented on Android")

    def is_modal_dialog(self, dialog):
        return True
