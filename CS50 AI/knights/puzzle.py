from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")
AClaimsKnight = Symbol("A claims to be a knight")
AClaimsKnave = Symbol("A claims to be a knave")
AClaimsSame = Symbol("A stated 'We are the same type'")
ALied =  Symbol("A told a lie")
ATruth =  Symbol("A told the truth")
ABClaimsKnave = Symbol("A claims B to be a knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")
BLied =  Symbol("B told a lie")
BTruth =  Symbol("B told the truth")
BClaimsDiff = Symbol("B stated 'We are different type'")
BAClaimsKnave = Symbol("B claims A to be a knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")
CAClaimsKnight = Symbol("C claims A to be a knave")

Same = Symbol("They are the same")
Different = Symbol("They are different")
#More of a showcase of thought variable than actual logic variable
Contradiction = Symbol("Always False")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Biconditional(ALied, AKnave),
    Or(AKnave, AKnight),
    Not(And(AKnave, AKnight)),
    AClaimsKnave, 
    AClaimsKnight,
    Implication(And(AClaimsKnave, AClaimsKnight, Not(And(AKnave, AKnight))), ALied),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Biconditional(ALied, AKnave),
    AClaimsKnave,
    #Either way for A to make knave claim A had to lie (although Knights cannot lie)
    Implication(AKnight, ALied),
    Implication(AKnave,ALied),
    ALied,
    ABClaimsKnave,
    Implication(And(ALied, ABClaimsKnave), BKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(ALied, AKnave),
    Biconditional(BLied, BKnave),
    Biconditional(BTruth, BKnight),
    AClaimsSame,
    BClaimsDiff,
    Implication(Same, And(ATruth, BLied)),
    Implication(Not(Same), And(ALied,BTruth)),
    #In order for the 1st implication to be true, it's conclusion would have to be false
    Implication(And(Same, And(ATruth, BLied)), Contradiction),
    Not(Same)

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Biconditional(ALied, AKnave),
    Biconditional(ATruth, AKnight),
    Biconditional(BLied, BKnave),
    Or(AClaimsKnave, AClaimsKnight),
    Implication(Not(AClaimsKnave), BLied),
    Implication(BKnave, CKnight),
    CAClaimsKnight,
    Implication(And(CAClaimsKnight, CKnight), AKnight),
    Implication(And(AKnave, AClaimsKnave), ATruth),
    Implication(And(ATruth, AKnave), Contradiction),
    Implication(And(AKnight, AClaimsKnave), ALied),
    Implication(And(ALied, AKnight), Contradiction),
    #Based on logic above, it is impossible for A to have claimed to have been a Knave
    Not(AClaimsKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
