import pytest

from widgetastic.widget import View
from widgetastic_patternfly4 import (
    FormSelect,
    FormSelectDisabled,
    FormSelectOptionDisabled,
    FormSelectOptionNotFound,
)


class FormSelectTestView(View):
    ROOT = ".//main[@role='main']"

    input = FormSelect(
        locator=".//h2[normalize-space(.)='Simple form select']/following-sibling::div[1]//select"
    )
    input_grouping = FormSelect(
        locator=".//h2[normalize-space(.)='Grouped form select']/following-sibling::div[1]//select"
    )
    input_invalid = FormSelect(
        locator=".//h2[normalize-space(.)='Invalid form select']/following-sibling::div[1]//select"
    )
    input_disabled = FormSelect(
        locator=".//h2[normalize-space(.)='Disabled form select']/following-sibling::div[1]//select"
    )


@pytest.fixture
def view(browser):
    return FormSelectTestView(browser)


def test_formselect_visibility(view):
    assert view.input.is_displayed
    assert view.input_grouping.is_displayed
    assert view.input_invalid.is_displayed
    assert view.input_disabled.is_displayed


def test_formselect_enablement(view):
    assert view.input.is_enabled
    assert view.input_grouping.is_enabled
    assert view.input_invalid.is_enabled
    assert not view.input_disabled.is_enabled


def test_formselect_validity(view):
    assert view.input.is_valid
    assert view.input_grouping.is_valid
    assert view.input_disabled.is_valid
    assert not view.input_invalid.is_valid
    view.input_invalid.fill('One')
    assert view.input_invalid.is_valid
    view.input_invalid.fill('Choose a number')
    assert not view.input_invalid.is_valid


def test_formselect_value(view):
    assert len(view.input.all_options) == 7
    assert len(view.input.all_enabled_options) == 6
    assert 'Mrs' in view.input.all_options
    view.input.fill('Mrs')
    assert view.input.read() == 'Mrs'


def test_formselect_option_enablement(view):
    expected_enabled_options = {'Mr', 'Miss', 'Mrs', 'Ms', 'Dr', 'Other'}
    expected_disabled_options = {'Please Choose'}
    assert set(view.input.all_enabled_options) == expected_enabled_options
    assert expected_disabled_options not in set(view.input.all_enabled_options)
    expected_enabled_optgroup_options = {
        'The First Option',
        'Second option is selected by default',
        'The Third Option',
        'The Fourth option'
    }
    expected_disabled_optgroup_options = {
        'The Fifth Option',
        'The Six option'
    }
    assert set(view.input_grouping.all_enabled_options) == expected_enabled_optgroup_options
    assert expected_disabled_optgroup_options not in set(view.input_grouping.all_enabled_options)


def test_formselect_fill_disabled_select(view):
    with pytest.raises(FormSelectDisabled):
        view.input_disabled.fill('Two')


def test_formselect_fill_disabled_option(view):
    with pytest.raises(FormSelectOptionDisabled):
        view.input_grouping.fill('The Fifth Option')


def test_formselect_fill_nonexistent_option(view):
    with pytest.raises(FormSelectOptionNotFound):
        view.input.fill('foo')
