__all__ = [
    'print_style'
]


def print_style(message, style='indented_separator'):
    """Print the given message with a specified style."""
    if style == 'box':
        style_chars = '#'
    elif style == 'section':
        style_chars = '='
    elif style == 'decorative':
        style_chars = '*'
    elif style == 'indented_separator':
        style_chars = '-'
    else:
        # Default to a simple line separator
        style_chars = '-'

    lines = message.split('\n')  # Split the multiline message into lines

    max_line_length = max(len(line) for line in lines)

    print(f"{style_chars * max_line_length}")
    for line in lines:
        # Pad shorter lines with spaces to match the maximum length
        print(f"{line.ljust(max_line_length)}")
    print(f"{style_chars * max_line_length}")
