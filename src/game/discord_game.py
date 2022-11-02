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
    last_response: hikari.Snowflake | None = None


@dataclasses.dataclass
class DiscordGame:
    """
    The discord-related information a game needs to store.
    """

    app: utils.Bot

    _interactions: tuple[Interaction | None, Interaction | None] = (None, None)

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
        await self.app.rest.execute_webhook(
            webhook=self.interactions[0].webhook_id,
            token=self.interactions[0].token,
            **kwargs,
        )

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
        self.interactions[player].last_response = msg.id

    async def delete_response(self, player: int) -> None:
        """Delete emphermial responses sent to both players."""

        inter = self.interactions[player]

        if not inter.last_response:
            return
        id = inter.last_response
        inter.last_response = None
        await self.app.rest.delete_webhook_message(
            webhook=inter.webhook_id,
            token=inter.token,
            message=id,
        )

    async def delete_responses(self) -> None:
        """Delete emphermial responses sent to both players."""
        await asyncio.gather(self.delete_response(0), self.delete_response(1))
