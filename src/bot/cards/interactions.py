from card import Card, Elements, Results

def interactions(card_1: Card, card_2: Card):
   if card_1.type - card_2.type == 2:
      return Results.P2_WIN

   if card_1.type - card_2.type == 3:
      return Results.P1_WIN

   if card_1.type - card_2.type in [0,1,4]:
      if card_1.value > card_2.value:
         return Results.P1_WIN

      if card_1.value < card_2.value:
         return Results.P2_WIN

      return Results.TIE

