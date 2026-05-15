import re

def preprocess(raw_logs):
    """
    Preprocess raw logs into a structured readable format for LLM input.
    
    Args:
        raw_logs (str or list): Raw log text or list of log lines.

    Returns:
        str: Cleaned and structured text summary.
    """

    if isinstance(raw_logs, str):
        lines = raw_logs.splitlines()
    else:
        lines = raw_logs

    log_entries = []

    log_pattern = re.compile(
        r'(?P<timestamp>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:,\d{3})?)?\s*'
        r'(?P<level>INFO|ERROR|WARN|WARNING|DEBUG|CRITICAL)?[:\s-]*'
        r'(?P<message>.*)', re.IGNORECASE
    )

    for line in lines:
        match = log_pattern.match(line)
        if match:
            timestamp = match.group('timestamp') or ''
            level = match.group('level') or 'LOG'
            message = match.group('message').strip()
            if message:
                formatted = f"[{level.upper()}] {timestamp} - {message}" if timestamp else f"[{level.upper()}] {message}"
                log_entries.append(formatted)

    if not log_entries:
        return "No useful log data extracted."

    return "\n".join(log_entries)
