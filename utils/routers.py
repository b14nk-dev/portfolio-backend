from typing import TypedDict

from fastapi import APIRouter


class RouteDict(TypedDict):
    path: str
    router: APIRouter


class Router:
    router: APIRouter
    name: str

    def __init__(self, router: APIRouter, name: str) -> None:
        self.router = router
        self.name = name
