import os

from xml.etree import ElementTree as ET

import click


def filter_reports_with_errors_or_failures(reports):

    result = dict()

    for report_path in reports.keys():
        attributes_list = list()
        for test_suite_attributes in reports[report_path]:
            if int(test_suite_attributes['errors']) or int(test_suite_attributes['failures']):
                attributes_list.append(test_suite_attributes)

        if attributes_list:
            result[report_path] = attributes_list

    return result


def _check_file_exists_and_is_readable(directory_entry):
    #return os.access(path, os.F_OK | os.R_OK)
    return directory_entry.is_file()


def _check_element_tree_has_expected_format(tree):
    return tree.getroot().tag == "testsuites" and len(tree.findall('testsuite'))


def _echo_dir_entry_paths(dir_entries):
    for dir_entry in dir_entries:
        click.echo(dir_entry.path)


def analyze_test_reports(test_report_entries):

    results = dict()

    for test_report_entry in test_report_entries:
        if not _check_file_exists_and_is_readable(test_report_entry):
            raise(ValueError(f"test report located at {test_report_entry.path} is not accessible"))

        element_tree = ET.parse(test_report_entry.path)

        if not _check_element_tree_has_expected_format(element_tree):
            raise(ValueError(f"Unsupported format found for {test_report_entry.path}"))

        results[test_report_entry.path] = list()

        for test_suite in element_tree.findall('testsuite'):
            results[test_report_entry.path].append(test_suite.attrib)

    return results


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

    results = analyze_test_reports(test_reports_dir_entries)

    reports_with_errors_or_failures = filter_reports_with_errors_or_failures(results)

    if reports_with_errors_or_failures:
        click.echo("JUnit test result reports with errors found:")
        _echo_dir_entry_paths(reports_with_errors_or_failures)
        raise SystemError("reports_with_errors_or_failures")

    else:
        click.echo("No JUnit test result reports with errors or failures found")


