from graphview.chunker import *

TEST_FILE_NAME = "file_name"
TEST_FILE_PATH = Path(f"{TEST_FILE_NAME}.md")


def prototype_test_file(input: list[str], expected_output: list[Chunk]) -> None:
    output = chapters_from_lines(input, TEST_FILE_PATH)
    assert output == expected_output


def test_empty():
    input = []
    expected_output = [Chunk(TEST_FILE_PATH, TEST_FILE_NAME, "", 0)]
    prototype_test_file(input, expected_output)


def test_h1_only():
    input = ["# This is the header"]
    expected_output = [
        Chunk(TEST_FILE_PATH, TEST_FILE_NAME, "", 0),
        Chunk(TEST_FILE_PATH, "This is the header", "", 1),
    ]
    prototype_test_file(input, expected_output)


def test_h1_only_no_space():
    input = ["#This is the header"]
    expected_output = [
        Chunk(TEST_FILE_PATH, TEST_FILE_NAME, "", 0),
        Chunk(TEST_FILE_PATH, "This is the header", "", 1),
    ]
    prototype_test_file(input, expected_output)

def test_improper_header():
    input = [" # Header"] # note space at start of line
    expected_output = [
        Chunk(TEST_FILE_PATH, TEST_FILE_NAME, " # Header", 0),
    ]
    prototype_test_file(input, expected_output)


def test_h1_with_content():
    input = ["# Header", "content"]
    expected_output = [
        Chunk(TEST_FILE_PATH, TEST_FILE_NAME, "", 0),
        Chunk(TEST_FILE_PATH, "Header", "content", 1),
    ]
    prototype_test_file(input, expected_output)

def test_h1_with_multi_line_content():
    input = ["# Header", "content 1", "content 2", "content 3"]
    expected_output = [
        Chunk(TEST_FILE_PATH, TEST_FILE_NAME, "", 0),
        Chunk(TEST_FILE_PATH, "Header", "content 1\ncontent 2\ncontent 3", 1),
    ]
    prototype_test_file(input, expected_output)


def test_multiple_headers():
    input = [
        "# Header 1",
        "# Header 2",
    ]
    expected_output = [
        Chunk(TEST_FILE_PATH, TEST_FILE_NAME, "", 0),
        Chunk(TEST_FILE_PATH, "Header 1", "", 1),
        Chunk(TEST_FILE_PATH, "Header 2", "", 2),
    ]
    prototype_test_file(input, expected_output)

def test_multiple_headers_with_content():
    input = [
        "# Header 1",
        "content 1",
        "# Header 2",
        "content 2",
        "# Header 3",
        "content 3",
    ]
    expected_output = [
        Chunk(TEST_FILE_PATH, TEST_FILE_NAME, "", 0),
        Chunk(TEST_FILE_PATH, "Header 1", "content 1", 1),
        Chunk(TEST_FILE_PATH, "Header 2", "content 2", 3),
        Chunk(TEST_FILE_PATH, "Header 3", "content 3", 5),
    ]
    prototype_test_file(input, expected_output)


def test_multiple_header_levels():
    input = [
        "# Header 1",
        "## Header 2",
    ]
    expected_output = [
        Chunk(TEST_FILE_PATH, TEST_FILE_NAME, "", 0),
        Chunk(TEST_FILE_PATH, "Header 1", "", 1),
        Chunk(TEST_FILE_PATH, "Header 2", "", 2),
    ]
    prototype_test_file(input, expected_output)

def test_metadata():
    input = [
        "---",
        "key: value",
        "---",
        "# Header"
    ]
    expected_output = [
        Chunk(TEST_FILE_PATH, TEST_FILE_NAME, "---\nkey: value\n---", 0),
        Chunk(TEST_FILE_PATH, "Header", "", 4),
    ]
    prototype_test_file(input, expected_output)