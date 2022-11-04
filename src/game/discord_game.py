import hikari
import dataclasses
import typing as t
import asyncio
import utils


@dataclasses.dataclass
class Interaction:
    """The minimum information needed to respond to an interaction."""

    webhook_id: hikari.Snowflake
    token: str
    ephermial_responses: list[hikari.Snowflake] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class DiscordGame:
    """
    The discord-related information a game needs to store.
    """

    app: utils.Bot

    _interactions: tuple[Interaction | None, Interaction | None] = (None, None)
    _global_response: hikari.Snowflake | None = None

    @property
    def interactions(self) -> tuple[Interaction, Interaction]:
        return self._interactions  # type: ignore

    def set_interaction(self, index: int, inter: hikari.PartialInteraction) -> None:
        """Set an interaction in the interaction tuple."""
        new = Interaction(
            webhook_id=inter.webhook_id,
            token=inter.token,
        )

        if index == 0:
            self._interactions = (new, self.interactions[1])
        else:
            self._interactions = (self.interactions[0], new)

    async def respond_global(self, **kwargs: t.Any) -> None:
        msg = await self.app.rest.execute_webhook(
            webhook=self.interactions[0].webhook_id,
            token=self.interactions[0].token,
            **kwargs,
        )
        self._global_response = msg.id

    async def edit_global(self, **kwargs: t.Any) -> None:
        if not self._global_response:
            raise ValueError("No global response has been made yet.")
        await self.app.rest.edit_webhook_message(
            webhook=self.interactions[0].webhook_id,
            token=self.interactions[0].token,
            message=self._global_response,
            **kwargs,
        )

    async def delete_global_response(self) -> None:
        if not self._global_response:
            raise ValueError("No global response has been made yet.")
        await self.app.rest.delete_webhook_message(
            webhook=self.interactions[0].webhook_id,
            token=self.interactions[0].token,
            message=self._global_response,
        )
        self._global_response = None

    async def respond_to_player(
        self,
        player: int,
        **kwargs: t.Any,
    ) -> None:
        """Send an ephermial response to a player."""
        msg = await self.app.rest.execute_webhook(
            webhook=self.interactions[player].webhook_id,
            token=self.interactions[player].token,
            **kwargs,
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        self.interactions[player].ephermial_responses.append(msg.id)

    async def delete_ephermial_responses(self) -> None:
        """Delete emphermial responses sent to both players."""

        async def delete_response(id: hikari.Snowflake, player: int) -> None:
            await self.app.rest.delete_webhook_message(
                webhook=self.interactions[player].webhook_id,
                token=self.interactions[player].token,
                message=id,
            )

        await asyncio.gather(
            *(delete_response(id, 0) for id in self.interactions[0].ephermial_responses),
            *(delete_response(id, 1) for id in self.interactions[1].ephermial_responses),
        )

        self.interactions[0].ephermial_responses = []
        self.interactions[1].ephermial_responses = []
