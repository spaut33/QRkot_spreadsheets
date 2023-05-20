from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
LOCALE = 'ru_RU'
SPREADSHEET_TITLE = 'Отчет на {now_date_time}'
SHEET_TITLE = 'Лист1'
ROW_COUNT = 100
COLUMN_COUNT = 11
SHEET_TYPE = 'GRID'
SHEET_ID = 0
MAJOR_DIMENSION = 'ROWS'
RANGE = 'A1:E30'
INPUT_OPTION = 'USER_ENTERED'
TABLE_HEADER = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание'],
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создаёт таблицу"""
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': SPREADSHEET_TITLE.format(
                now_date_time=datetime.now().strftime(FORMAT)
            ),
            'locale': LOCALE,
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': SHEET_TYPE,
                    'sheetId': SHEET_ID,
                    'title': SHEET_TITLE,
                    'gridProperties': {
                        'rowCount': ROW_COUNT,
                        'columnCount': COLUMN_COUNT,
                    },
                }
            }
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


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
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = TABLE_HEADER[:]
    table_values[0][1] = now_date_time
    table_values.extend(
        [
            [
                str(project['name']),
                str(project['duration']),
                str(project['description']),
            ]
            for project in charity_projects
        ]
    )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=RANGE,
            valueInputOption=INPUT_OPTION,
            json={'majorDimension': MAJOR_DIMENSION, 'values': table_values},
        )
    )
