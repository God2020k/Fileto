# utils_bot.py

def get_readable_file_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} PB"

def readable_time(seconds: int) -> str:
    count = 0
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        if count == 0:
            remainder, result = divmod(seconds, 60)
        elif count == 1:
            remainder, result = divmod(remainder, 60)
        elif count == 2:
            remainder, result = divmod(remainder, 24)
        else:
            result = remainder
        if result != 0:
            time_list.append(f"{int(result)}{time_suffix_list[count]}")
        count += 1

    return " ".join(reversed(time_list))
