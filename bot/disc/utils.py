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
