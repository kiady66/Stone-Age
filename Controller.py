from typing import cast, Callable, List, Dict

import Action
from Farmable.Farmable import Resource
from Game.Game import Game, State
from Place import AbstractPlace


class Controller:
    def __init__(self):
        self.game: Game = None
        self.on_place_event_action: Callable[[], (AbstractPlace, int)] = None
        self.on_take_event_action: Callable[[], AbstractPlace] = None
        self.on_use_tool_event_action: Callable[[], int] = None
        self.let_meeple_event_action: Callable[[], bool] = None
        self.choose_between_lose_points_or_resources_event_action: Callable[[], bool] = None
        self.on_pay_resource_event_action: Callable[[], str] = None

    def on_place_event(self, possible_actions: List[Action.Action]) -> Action.Action:
        while True:
            (place, n) = self.on_place_event_action()
            if place is not None and n is not None:
                break
        for a in possible_actions:
            if a.action_type == Action.ActionType.PLACE_MEEPLES:
                a = cast(Action.PlaceMeeplesAction, a)
                if a.place == place and a.nb_meeple == n:
                    return a

    def on_take_event(self, possible_actions: List[Action.Action]) -> Action.Action:
        while True:
            place = self.on_take_event_action()
            if place is not None:
                break
        for a in possible_actions:
            if a.action_type == Action.ActionType.TAKE_MEEPLES:
                a = cast(Action.TakeMeeplesAction, a)
                if a.place == place:
                    return a

    def on_use_tool_event(self, possible_actions: List[Action.Action]) -> Action.Action:
        if len(possible_actions) == 1:  # One action == the 0 tool usage
            return possible_actions[0]
        while True:
            tool_number = self.on_use_tool_event_action()
            if tool_number is not None:
                break
        for a in possible_actions:
            if a.action_type == Action.ActionType.USE_TOOL and cast(Action.UseToolAction,
                                                                    a).nb_tools == tool_number:
                return a

    def let_meeple_event(self, possible_actions: List[Action.Action]) -> Action.Action:
        while True:
            let_meeple = self.let_meeple_event_action()
            if let_meeple is not None:
                break
        if not let_meeple:
            return
        for a in possible_actions:
            if a.action_type == Action.ActionType.LET_ALL_MEEPLES:
                return a

    def choose_between_lose_points_or_resources_event(self, possible_actions: List[Action.Action]) -> Action.Action:
        while True:
            pay_resources = self.choose_between_lose_points_or_resources_event_action()
            if pay_resources is not None:
                break
        for a in possible_actions:
            if a.action_type == Action.ActionType.PAY_RESOURCE_OR_POINTS and cast(Action.PayResourceOrPointsAction,
                                                                                  a).pay_resource == pay_resources:
                return a

    def on_pay_resource_event(self, possible_actions: List[Action.Action]) -> Action.Action:
        while True:
            resource_name = self.on_pay_resource_event_action()
            if resource_name is not None:
                break
        for a in possible_actions:
            if a.action_type == Action.ActionType.PAY_SINGLE_RESOURCE_COST and cast(Action.PaySingleResourceAction,
                                                                                    a).resource.name == resource_name:
                return a
