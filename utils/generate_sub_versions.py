import random
from difflib import SequenceMatcher


DEFAULT_FREQUENCY = 1 / 30


def generate_sub_versions(start_version, end_version, frequency=DEFAULT_FREQUENCY):
    """
    Generate intermediary versions between 2 versions of the same text, by applying successively 'insert' and 'delete'
    modifications from the diff between start and end versions.

    Args:
        start_version (str): text version from which to start
        end_version (str): text version to transform into
        frequency (float): sampling ratio for sub-versions

    Returns:
        List[str]: list of sampled sub-versions, beginning by start version but not necessarily ending with end version

    """
    sub_versions = [start_version]
    current_version = start_version
    while current_version != end_version:
        sequence_matcher = SequenceMatcher(None, current_version, end_version)

        for tag, i1, i2, j1, j2 in sequence_matcher.get_opcodes():
            if tag != 'equal':
                text_before = current_version[:i1]
                text_after = current_version[i2:]

                if tag in ['delete', 'replace']:
                    text_to_delete = current_version[i1:i2]
                    for i in range(len(text_to_delete)):
                        current_version = text_before + text_to_delete[i + 1:] + text_after
                        if random.random() < frequency:
                            sub_versions.append(current_version)

                if tag in ['insert', 'replace']:
                    text_to_insert = end_version[j1:j2]
                    for i in range(len(text_to_insert)):
                        current_version = text_before + text_to_insert[:i + 1] + text_after
                        if random.random() < frequency:
                            sub_versions.append(current_version)

                break

    return sub_versions


def generate_all_sub_versions_from_list(versions, frequency=DEFAULT_FREQUENCY):
    """
    Generate intermediary versions based on several checkpoint versions of the same text.
    Args:
        versions (List[str]): list of all checkpoint versions
        frequency (float): sampling ratio for sub-versions

    Returns:
        (List[str]): list of all sampled sub-versions, including also all checkpoint versions
    """
    sub_versions = [
        sub_version
        for version, next_version in zip(versions, versions[1:])
        for sub_version in generate_sub_versions(version, next_version, frequency)
    ]
    sub_versions.append(versions[-1])

    return sub_versions
