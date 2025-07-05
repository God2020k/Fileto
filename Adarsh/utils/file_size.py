def get_readable_file_size(size: int) -> str:
    # Converts bytes to human-readable string
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def readable_time(seconds: int) -> str:
    # Converts seconds to human-readable uptime string
    count = 0
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and result == 0:
            break
        time_list.append(f"{int(result)}{time_suffix_list[count - 1]}")
        seconds = int(remainder)

    return ":".join(reversed(time_list))
