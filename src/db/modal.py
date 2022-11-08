from __future__ import annotations

import apgorm
import apgorm.types


class PlayerModel(apgorm.Model):
    id = apgorm.types.BigInt().field()
    decks = apgorm.types.Json().field()
    cards = apgorm.types.Array(apgorm.types.Int()).field()

    primary_key = (id,)
