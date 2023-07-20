import re
from typing import Dict


def ping(user_id: str) -> str:
    return f'<@{user_id}>'


def stat_dict_to_message(stat_dict: Dict[str, str]):
    converted_dict = {int(k): int(v) for k, v in stat_dict.items()}
    message = ''
    message += f'Total games: {sum(converted_dict.values())}' + '\n'
    message += f'Wins: {converted_dict[1] + converted_dict[2]}' + '\n'
    message += f'Losses: {converted_dict[-1] + converted_dict[-2]}' + '\n'
    message += f'Draws: {converted_dict[0]}'
    return message


def id_from_ping(ping_text):
    id_regex = re.compile('^<@(.+)>$')
    return id_regex.match(ping_text).group(1)


def parse_colon_arguments(arg_list):
    separator_regex = re.compile("( *(against|server|from|to|channel): *(\S+) *)")
    args = separator_regex.findall(arg_list)
    return {arg[1]: arg[2] for arg in args}