from dataclasses import dataclass
from pprint import pprint as pp
from typing import TypedDict, Literal, Annotated
from uuid import uuid4

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(
        {
            "apiversion": "1",
            "author": "zevaverbach",
            "head": "default",
            "color": "#E1AD01",
            "tail": "default",
            "version": "0.0.1-beta",
        }
    )


@app.route("/start", methods=["POST"])
def start():
    return "hi", 200


class Squad(TypedDict):
    allowBodyCollisions: bool
    sharedElimination: bool
    sharedHealth: bool
    sharedLength: bool


class Royale(TypedDict):
    shrinkEveryNTurns: int


@dataclass
class ValueRange:
    min: int
    max: int


class Settings(TypedDict):
    foodSpawnChance: Annotated[int, ValueRange(0, 10)]
    hazardDamagePerTurn: int
    minimumFood: int
    royale: Royale
    squad: Squad


class Ruleset(TypedDict):
    name: Literal["standard", "solo", "royale", "squad", "constrictor"]
    settings: Settings
    version: str


class Game(TypedDict):
    id: uuid4
    ruleset: Ruleset
    source: str
    timeout: Annotated[int, "milliseconds"]


class Coordinate(TypedDict):
    x: int
    y: int


class Snake(TypedDict):
    body: list[Coordinate]
    head: Coordinate
    health: Annotated[int, ValueRange(0, 100)]
    id: str
    latency: int
    length: int
    name: str
    shout: str
    squad: str


class Board(TypedDict):
    food: list[Coordinate]
    hazards: list[Coordinate]
    height: int
    width: int
    snakes: list[Snake]


Move = Literal["up", "down", "left", "right"]


@app.route("/move", methods=["POST"])
def move():
    game_info = request.get_json()
    game: Game = game_info["game"]
    turn: int = game_info["turn"]
    board: Board = game_info["board"]
    you: Snake = game_info["you"]

    # TODO: cache active games using the ID
    # TODO: determine the direction of all players, including yoruself
    #   this should be possible from the start if the snakes are
    #   all pointing straight, their heads will be at the front
    #   and pointing the direction they're traveling in.
    # TODO: instantiate the snake instances at the start

    player_class = get_player_class(game["ruleset"]["name"])
    player = player_class(you)
    move: Move = player.get_move(board)

    return jsonify({"move": "up"})


@app.route("/end", methods=["POST"])
def end():
    return "hi", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
