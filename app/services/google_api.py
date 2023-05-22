import copy
from datetime import datetime
from typing import Tuple

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_TITLE = 'Отчет на {now_date_time}'
MAJOR_DIMENSION = 'ROWS'
INPUT_OPTION = 'USER_ENTERED'
ROW_COUNT = 100
COLUMN_COUNT = 11
TABLE_HEADER = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]
SPREADSHEET_BODY = dict(
    properties=dict(title='', locale='ru_RU'),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(rowCount=ROW_COUNT, columnCount=COLUMN_COUNT),
    ))],
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> Tuple[str, str]:
    """Создаёт таблицу"""
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = copy.deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = SPREADSHEET_TITLE.format(
        now_date_time=datetime.now().strftime(FORMAT)
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
    spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    """Устанавливает права доступа к таблице"""
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str, charity_projects: list, wrapper_services: Aiogoogle
) -> None:
    """Записывает данные в таблицу"""
    service = await wrapper_services.discover('sheets', 'v4')
    table_header = copy.deepcopy(TABLE_HEADER)
    table_header[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *table_header,
        *[list(map(str, project.values())) for project in charity_projects],
    ]
    row_count = len(table_values)
    column_count = len(max(table_values, key=len))
    if row_count > ROW_COUNT:
        raise ValueError(
            'Количество строк превышает допустимое значение: '
            f'Максимально: {ROW_COUNT}, передано: {row_count}'
        )
    if column_count > COLUMN_COUNT:
        raise ValueError(
            'Количество столбцов превышает допустимое значение:'
            f'Максимально: {COLUMN_COUNT}, передано: {column_count}'
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=(
                f'R1C1:R{row_count}C{column_count}'
            ),
            valueInputOption=INPUT_OPTION,
            json={'majorDimension': MAJOR_DIMENSION, 'values': table_values},
        )
    )
