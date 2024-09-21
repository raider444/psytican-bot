from src.telegram.tg_wrapper import event_list

from tests.src.telegram.cases.success import success_event_list_model_render_0


def test_event_list():
    calendar_data = success_event_list_model_render_0.calendar_data
    result_data = success_event_list_model_render_0.result_data
    assert event_list(events=calendar_data) == result_data
