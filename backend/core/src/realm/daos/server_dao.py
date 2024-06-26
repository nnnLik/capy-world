from dataclasses import dataclass
from datetime import datetime

from src.realm.models import Server, ServerMember


@dataclass(frozen=True, slots=True)
class CreateServerDTO:
    admin_id: int
    name: str
    description: str | None
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ServerDTO:
    id: int
    admin_id: int
    name: str
    created_at: datetime
    description: str | None = None


@dataclass(frozen=True, slots=True)
class UserServersDTO:
    servers: list[ServerDTO]


class ServerDAO:
    def create_user_server(
        self,
        admin_id: int,
        name: str,
        description: str | None = None,
    ) -> CreateServerDTO:
        server = Server.objects.create(
            admin_id=admin_id,
            name=name,
            description=description,
        )
        ServerMember.objects.create(
            server=server,
            user_id=admin_id,
        )

        return CreateServerDTO(
            admin_id=server.admin_id,
            name=server.name,
            description=server.description,
            created_at=server.created_at,
        )

    def check_if_user_already_joined(
        self,
        server_id: int,
        user_id: int,
    ) -> bool:
        return ServerMember.objects.filter(
            server_id=server_id, user_id=user_id
        ).exists()

    def connect_user_to_server(
        self,
        server_id: int,
        user_id: int,
    ) -> None:
        ServerMember.objects.create(
            server_id=server_id,
            user_id=user_id,
        )

    def get_user_servers(self, user_id: int) -> UserServersDTO:
        server_ids = ServerMember.objects.values('server_id').filter(user_id=user_id)
        servers = Server.objects.values().filter(id__in=server_ids)

        return UserServersDTO(
            servers=[
                ServerDTO(
                    id=server.id,
                    admin_id=server.admin_id,
                    description=server.description,
                    name=server.name,
                    created_at=server.created_at,
                )
                for server in servers
            ],
        )
