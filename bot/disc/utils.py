import re
from typing import Dict, Sequence


def ping(user_id: str) -> str:
    return f'<@{user_id}>'


def stat_dict_to_message(stat_dict: Dict[str, str], mode='concise'):
    converted_dict = {int(k): int(v) for k, v in stat_dict.items()}
    message = ''
    message += f'Total games: {sum(converted_dict.values())}' + '\n'
    if mode == 'concise':
        message += f'Wins: {converted_dict[1] + converted_dict[2]}' + '\n'
        message += f'Losses: {converted_dict[-1] + converted_dict[-2]}' + '\n'
    elif mode == 'verbose':
        message += f'Wins by position: {converted_dict[1]}' + '\n'
        message += f'Wins by resignation: {converted_dict[2]}' + '\n'
        message += f'Losses by position: {converted_dict[-1]}' + '\n'
        message += f'Losses by resignation: {converted_dict[-2]}' + '\n'
    message += f'Draws: {converted_dict[0]}'
    return message


def user_id_from_mention(mention):
    id_regex = re.compile('^<@(.+)>$')
    return id_regex.match(mention).group(1)


def channel_id_from_mention(mention):
    id_regex = re.compile('^<#(.+)>$')
    return id_regex.match(mention).group(1)


def parse_colon_arguments(arg_list: str, options: Sequence[str]):
    option_regex = '|'.join(options)

    # example: "( *(against|server|from|to|channel|mode): *(\S+) *)"
    # if options = ['against', 'server', 'from', 'to', 'channel', 'mode']
    separator_regex = re.compile(f"( *({option_regex}): *(\S+) *)")
    args = separator_regex.findall(arg_list)
    return {arg[1]: arg[2] for arg in args}
