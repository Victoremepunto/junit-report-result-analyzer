import os

from junitparser import JUnitXml


import click


def check_if_errors_or_failures(xml):

    for test_suite in xml:
        if test_suite.errors or test_suite.failures:
            return True

    return False


def _check_file_exists_and_is_readable(directory_entry):
    return directory_entry.is_file()


def _check_element_tree_has_expected_format(tree):
    return tree.getroot().tag == "testsuites" and len(tree.findall('testsuite'))


def _echo_dir_entry_paths(dir_entries):
    for dir_entry in dir_entries:
        click.echo(dir_entry.path)


def get_single_xml(test_report_entries):

    xml = JUnitXml()

    for test_report_entry in test_report_entries:
        if not test_report_entry.is_file():
            raise(ValueError(f"test report located at {test_report_entry.path} is not accessible"))

        xml += JUnitXml.fromfile(test_report_entry.path)

    return xml


@click.command()
@click.argument('path', default='.')
def cli(path):

    click.echo(f"Looking for JUnit test result reports on path '{path}'")
    test_reports_dir_entries = [report for report in os.scandir(path)
                          if report.name.startswith('junit-') and report.name.endswith('.xml')]
    if not test_reports_dir_entries:
        click.echo(f"No JUnit test result reports found on '{path}'")
        return
    else:
        click.echo(f"list of JUnit test result reports to be analyzed:")
        _echo_dir_entry_paths(test_reports_dir_entries)

    xml = get_single_xml(test_reports_dir_entries)

    if check_if_errors_or_failures(xml):
        click.echo("JUnit test result reports with errors found:")
        # _echo_dir_entry_paths(reports_with_errors_or_failures)
        raise SystemError("reports_with_errors_or_failures")

    else:
        click.echo("No JUnit test result reports with errors or failures found")


