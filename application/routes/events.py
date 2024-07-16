import aiohttp
from slugify import slugify
from aiosqlite import Error
from pydantic import ValidationError
from sanic import Blueprint, response, text
from sanic.request import Request
from sanic.exceptions import NotFound, InvalidUsage
from application.database.db import execute_query, fetch_all, fetch_one
from application.schemas.schemas import EventCreate, EventUpdate

events_bp = Blueprint('events', url_prefix='/events')

SPORTS_DB_API_URL = "https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t="

async def fetch_logo(team_name):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(SPORTS_DB_API_URL + team_name) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data['teams']:
                        return data['teams'][0]['strTeamLogo']
        except Exception as e:
            print(f"Error fetching logo for {team_name}: {e}")
    return None

async def get_all_events_from_db(db):
    query = "SELECT * FROM event"
    return await fetch_all(db, query)

async def get_event_by_id_from_db(db, event_id):
    query = "SELECT * FROM event WHERE id = ?"
    return await fetch_one(db, query, (event_id,))

async def create_event_in_db(db, event_data):
    query = """
        INSERT INTO event (name, active, slug, type, status, start_time, actual_start_time, sport_id, logos)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        event_data.get('name'),
        event_data.get('active', 1),
        event_data.get('slug'),
        event_data.get('type'),
        event_data.get('status'),
        event_data.get('start_time'),
        event_data.get('actual_start_time'),
        event_data.get('sport_id'),
        event_data.get('logos')
    )
    await execute_query(db, query, params)
    # Fetch the last inserted event to return
    query = "SELECT * FROM event WHERE id = last_insert_rowid()"
    return await fetch_one(db, query)

async def update_event_in_db(db, event_id, event_data):
    query = """
        UPDATE event
        SET name = ?, active = ?, slug = ?, type = ?, status = ?, start_time = ?, actual_start_time = ?, sport_id = ?, logos = ?
        WHERE id = ?
    """
    params = (
        event_data.get('name'),
        event_data.get('active', 1),
        event_data.get('slug'),
        event_data.get('type'),
        event_data.get('status'),
        event_data.get('start_time'),
        event_data.get('actual_start_time'),
        event_data.get('sport_id'),
        event_data.get('logos'),
        event_id
    )
    await execute_query(db, query, params)
    # Fetch the updated event to return
    return await get_event_by_id_from_db(db, event_id)

async def delete_event_in_db(db, event_id):
    query = "DELETE FROM event WHERE id = ?"
    await execute_query(db, query, (event_id,))
    # Check if the event was actually deleted
    deleted_event = await get_event_by_id_from_db(db, event_id)
    return deleted_event is None

@events_bp.route('/', methods=['GET'])
async def get_all_events(request: Request):
    db = request.app.ctx.db
    events = await get_all_events_from_db(db)
    return response.json(events)

@events_bp.route('/<event_id:int>', methods=['GET'])
async def get_event_by_id(request: Request, event_id: int):
    db = request.app.ctx.db
    event = await get_event_by_id_from_db(db, event_id)
    if event:
        return response.json(event)
    else:
        raise NotFound('Event not found')

@events_bp.route('/', methods=['POST'])
async def create_event(request: Request):
    try:
        event_data = EventCreate(**request.json).model_dump()
        if not event_data.get("slug"):
            event_data["slug"] = slugify(event_data["name"])
    except ValidationError as e:
        return response.json({"message": f"Invalid data: {e.errors()}"}, 400)

    # Fetch logos for the teams
    teams = event_data['name'].split(' v ')
    if len(teams) == 2:
        team1_logo = await fetch_logo(teams[0].strip())
        team2_logo = await fetch_logo(teams[1].strip())
        logos = f"{team1_logo or ''}|{team2_logo or ''}"
        if not team1_logo and not team2_logo:
            logos = None
        event_data['logos'] = logos
    else:
        event_data['logos'] = None

    db = request.app.ctx.db
    try:
        created_event = await create_event_in_db(db, event_data)
        return response.json(created_event, status=201)
    except Error as e:
        return response.json({"message": f"An error occurred: {e}"}, 500)

@events_bp.route('/<event_id:int>', methods=['PUT'])
async def update_event(request: Request, event_id: int):
    try:
        event_data = EventUpdate(**request.json).model_dump()
    except ValidationError as e:
        return response.json({"message": f"Invalid data: {e.errors()}"}, 400)

    db = request.app.ctx.db
    updated_event = await update_event_in_db(db, event_id, event_data)
    if updated_event:
        return response.json(updated_event)
    else:
        raise NotFound('Event not found')

@events_bp.route('/<event_id:int>', methods=['DELETE'])
async def delete_event(request: Request, event_id: int):
    db = request.app.ctx.db
    success = await delete_event_in_db(db, event_id)
    if success:
        return text('', 204)
    else:
        raise NotFound('Event not found')
