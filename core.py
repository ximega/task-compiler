class Keywords:
    DEFINE='define'
    FIND='find'
    FINDF='findf'
    RESPONSE='response'
    NAME='name'
    MODE='mode'

class Commands:
    COMPILE='compile'
    SHOW='show'
    CLEAR='cls'
    INFO='info'

class ModsC:
    PHYSICS='-p'
    GEOMETRY='-g'
    RESULT='-r'
    FORMULA='-f'

class ModsF:
    CENTRAL_POINT='-central-point'

class Formulas:
    CIRCLE_AREA='PI * R ** 2'
    CIRCUMFERENCE='2 * PI * R'
    ARC_LENGTH='alpha * R'
    TO_ANGLE='180 / PI * alpha'
    TO_RADIAN='PI / 180 * alpha'

formulas = {
    "CIRCLE_AREA": """
        R - radius
    """,
    "CIRCUMFERENCE": """
        R - radius
    """,
    "ARC_LENGTH": """
        alpha - angle (rad)
        R - radius
    """,
    "TO_ANGLE": """
        alpha - angle (rad)
    """,
    "TO_RADIAN": """
        alpha - angle (degrees)
    """
}