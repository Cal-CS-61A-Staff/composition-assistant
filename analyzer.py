import ast
from typing import Dict, List, Generator, Type, NamedTuple
from stringcase import snakecase

hog = {
   "roll_dice": ["def roll_dice", "def free_bacon"],
   "play": ["def play", "#######################"],
   "max_scoring_num_rolls": ["def max_scoring_num_rolls", "def winner"],
}

cats = {
    "accuracy": ["def accuracy", "def wpm"],
    "autocorrect": ["def autocorrect", "def shifty_shifts"],
    "fastest_words": ["def fastest_words(", "def game"]
}

ants = {
    "Short and LongThrowers": ["class ShortThrower", "class FireAnt"],
    "ThrowerAnt": ["class ThrowerAnt", "def throw_at"],
    "FireAnt": ["class FireAnt", "class WallAnt"],
}

PROBLEM = {
  "ants": ants,
  "cats": cats,
  "hog": hog
}

class Comment(NamedTuple):
    line_num: int
    comment: str
    fields: List[str] = []


class Problem(NamedTuple):
    code: str
    initial_line_number: int
    comments: List[Comment]


def checker(cls):
    CHECKERS.append(cls)
    return cls


def question_checker(q):
    def checker(cls):
        if q not in TARGETED_CHECKERS:
            TARGETED_CHECKERS[q] = []
        TARGETED_CHECKERS[q].append(cls)
        return cls

    return checker


class Checker(ast.NodeVisitor):
    def comments(self) -> Generator[Comment, None, None]:
        yield NotImplemented


CHECKERS: List[Type[Checker]] = []
TARGETED_CHECKERS: Dict[str, List[Type[Checker]]] = {}


def get_problems(code: str):
    from cli import proj
    problems = PROBLEM[proj]
    out = {}
    for name, (start, end) in problems.items():
        start_index = code.index(start)
        end_index = code.index(end)
        initial_line_number = code[:start_index].count("\n") + 1
        func_code = code[start_index:end_index].strip()

        comments = []

        tree = ast.parse(func_code)
        for checker in CHECKERS + TARGETED_CHECKERS.get(name, []):
            checker = checker(func_code)
            checker.visit(tree)
            for comment in checker.comments():
                comments.append(
                    Comment(
                        comment.line_num + initial_line_number - 1,
                        comment.comment,
                        comment.fields,
                    )
                )

        comments.sort(key=lambda x: x.line_num)

        out[name] = Problem(func_code, initial_line_number, comments)
    return out


# @checker
class VariableNotNeededChecker(Checker):
    class Variable:
        def __init__(self):
            self.initialized = 0
            self.accessed = 0
            self.line_num = 100000000000000000

    def __init__(self, code):
        self.variables: Dict[str, VariableNotNeededChecker.Variable] = {}

    def comments(self):
        for name, var in self.variables.items():
            if not var.initialized:
                continue
            if var.initialized == 1 and var.accessed == 1:
                yield Comment(
                    var.line_num,
                    f"The variable `{name}` is only accessed once, "
                    f"so it would be cleaner to just use its value directly.",
                )
            elif var.accessed == 0:
                yield Comment(
                    var.line_num,
                    f"The variable `{name}` is not accessed "
                    f"so you should remove it, since it is not used in the program.",
                )

    def visit_Name(self, node):
        name, context = node.id, node.ctx
        if name not in self.variables:
            self.variables[name] = self.Variable()
        var = self.variables[name]
        if isinstance(context, ast.Store):
            var.initialized += 1
            var.line_num = min(var.line_num, node.lineno)
        if isinstance(context, ast.Load):
            var.accessed += 1
            if not var.initialized:
                var.line_num = min(var.line_num, node.lineno)
        self.generic_visit(node)


@checker
class MeaningfulVariableNameChecker(Checker):
    class Variable:
        def __init__(self):
            self.count = 0
            self.line_num = 100000000000000000

    def __init__(self, code):
        self.variables: Dict[str, MeaningfulVariableNameChecker.Variable] = {}

    def comments(self):
        for name, var in self.variables.items():
            yield Comment(
                var.line_num,
                f"The name `{name}` is not descriptive and makes the code more difficult for somebody else to "
                f"understand. Using names like `{{alternative}}` would clarify what the name represents.",
                ["alternative"],
            )

    def visit_Name(self, node):
        name, context = node.id, node.ctx
        if len(name) < 3:
            if name not in self.variables:
                self.variables[name] = self.Variable()
            var = self.variables[name]
            var.count += 1
            var.line_num = min(var.line_num, node.lineno)
        self.generic_visit(node)


@question_checker("roll_dice")
class MultipleLoopChecker(Checker):
    def __init__(self, code):
        self.loop_cnt = 0

    def comments(self):
        if self.loop_cnt > 1:
            yield Comment(
                0,
                "Having multiple loops makes the code more complicated than it should be. "
                "Instead, the code could have a boolean flag that becomes true when a call to `dice()` is 1. "
                "At the end, return the total of outcomes or 1 depending on the boolean flag after the loop. "
                "By keeping the behavior similar to both pig out and non pig out cases, the code is greatly simplified.",
            )

    def visit_While(self, node):
        self.loop_cnt += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.loop_cnt += 1
        self.generic_visit(node)


@checker
class AugmentedAssignmentChecker(Checker):
    def __init__(self, code):
        self.code = code
        self._comments = []

    def comments(self):
        yield from self._comments

    def visit_Assign(self, node):
        targets, value = node.targets, node.value
        if (
            len(targets) == 1
            and isinstance(targets[0], ast.Name)
            and isinstance(value, ast.BinOp)
            and isinstance(value.left, ast.Name)
            and value.left.id == targets[0].id
        ):
            op = value.op
            if isinstance(op, ast.Add):
                op = "+"
            elif isinstance(op, ast.Sub):
                op = "-"
            elif isinstance(op, ast.Mult):
                op = "*"
            elif isinstance(op, ast.Div):
                op = "/"
            elif isinstance(op, ast.FloorDiv):
                op = "//"
            elif isinstance(op, ast.Pow):
                op = "**"
            if isinstance(op, str):
                full_line = self.code.split("\n")[node.lineno - 1].strip()
                lhs, rhs = full_line.split("=", 1)
                lhs_repeat, real_rhs = rhs.split(op)
                self._comments.append(
                    Comment(
                        node.lineno,
                        f"Don't forget that `{lhs.strip()} {op}= {real_rhs.strip()}` is a cleaner way "
                        f"of writing `{lhs}={lhs_repeat}{op}{real_rhs}`",
                    )
                )
        self.generic_visit(node)


@checker
class BuiltinShadowingChecker(Checker):
    BUILTINS = ["sum", "dict", "map", "range", "max", "min"]

    class Variable:
        def __init__(self):
            self.line_num = 100000000000000000

    def __init__(self, code):
        self.variables: Dict[str, BuiltinShadowingChecker.Variable] = {}

    def comments(self):
        for name, var in self.variables.items():
            yield Comment(
                var.line_num,
                f"The name `{name}` is actually a built-in Python function "
                f"(which is why it appears in a different color in most text editors). "
                f"When assigning a value to `{name}`, the code is actually overriding builtin Python functionality, "
                f"which could lead to trouble sometimes! A different name you can use is `{{alternative}}`.",
                ["alternative"],
            )

    def visit_Name(self, node):
        name, context = node.id, node.ctx
        if isinstance(node.ctx, ast.Store) and name in self.BUILTINS:
            if name not in self.variables:
                self.variables[name] = self.Variable()
            var = self.variables[name]
            var.line_num = min(var.line_num, node.lineno)
        self.generic_visit(node)


@checker
class UnnecessaryBooleanComparison(Checker):
    def __init__(self, code):
        self.code = code
        self._comments = []

    def comments(self):
        yield from self._comments

    def visit_Compare(self, node):
        if len(node.ops) == 1:
            op = node.ops[0]
            right = node.comparators[0]
            if isinstance(op, (ast.Eq, ast.Is, ast.NotEq, ast.IsNot)) and isinstance(
                right, ast.NameConstant
            ):
                is_truthy = isinstance(op, (ast.NotEq, ast.IsNot)) != (
                    right.value is True
                )
                full_line = self.code.split("\n")[node.lineno - 1].strip()
                if isinstance(op, ast.Eq):
                    op = "=="
                elif isinstance(op, ast.NotEq):
                    op = "!="
                elif isinstance(op, ast.Is):
                    op = "is"
                elif isinstance(op, ast.IsNot):
                    op = "is not"
                true_target = (
                    ("not `None`" if is_truthy else "`None`")
                    if right.value is None
                    else "`True`"
                    if is_truthy
                    else "`False`"
                )
                has_not = "" if is_truthy else "not "
                target = str(right.value)
                self._comments.append(
                    Comment(
                        node.lineno,
                        f"Can you simplify the comparison in `{full_line}`? "
                        f"Remember that you can check whether an expression is {true_target} using syntax like "
                        f"`if {has_not}<expr>: ...`, rather than `if <expr> {op} {target}: ...`",
                    )
                )
        self.generic_visit(node)


@checker
class ThisInVariableNameChecker(Checker):
    class Variable:
        def __init__(self):
            self.line_num = 100000000000000000

    def __init__(self, code):
        self.variables: Dict[str, ThisInVariableNameChecker.Variable] = {}

    def comments(self):
        for name, var in self.variables.items():
            yield Comment(
                var.line_num,
                f"Kind of nitpicky, but `{name}` is a slightly verbose name. We might be able to make do with just "
                f"`{{alternative}}` since it carrries the same semantic value. In languages other than Python, the term "
                f"`this` has different meaning which might confuse people who might not be as familiar with Python but "
                f"are still trying to understand the code.",
                ["alternative"],
            )

    def visit_Name(self, node):
        name, context = node.id, node.ctx
        if isinstance(node.ctx, ast.Store) and "this" in name:
            if name not in self.variables:
                self.variables[name] = self.Variable()
            var = self.variables[name]
            var.line_num = min(var.line_num, node.lineno)
        self.generic_visit(node)


@checker
class LongVariableNameChecker(Checker):
    class Variable:
        def __init__(self):
            self.line_num = 100000000000000000

    def __init__(self, code):
        self.variables: Dict[str, LongVariableNameChecker.Variable] = {}

    def comments(self):
        for name, var in self.variables.items():
            yield Comment(
                var.line_num,
                f"Let's try to convey the same message in fewer characters because, the longer a name is, the more "
                f"time a programmer needs to spend parsing and understanding its role in the function. For example, "
                f"we can simplify `{name}` to just `{{alternative}}`.",
                ["alternative"],
            )

    def visit_Name(self, node):
        name, context = node.id, node.ctx
        if (
            name != "implemented"
            and isinstance(node.ctx, ast.Store)
            and (max(len(part) for part in name.split("_")) > 10 or len(name) > 25)
        ):
            if name not in self.variables:
                self.variables[name] = self.Variable()
            var = self.variables[name]
            var.line_num = min(var.line_num, node.lineno)
        self.generic_visit(node)


@checker
class UnnecessaryRangeArgumentChecker(Checker):
    def __init__(self, code):
        self._comments = []

    def comments(self):
        yield from self._comments

    def visit_Call(self, node):
        func, args = node.func, node.args
        if (
            isinstance(func, ast.Name)
            and func.id == "range"
            and args
            and isinstance(args[0], ast.Num)
            and args[0].n == 0
        ):
            self._comments.append(
                Comment(
                    node.lineno,
                    f"Nitpick: if you’re iterating over a range of numbers starting from 0, there’s no need to specify "
                    f"your starting point i.e. `range(0, X) = range(X)`",
                )
            )
        self.generic_visit(node)


@checker
class CamelCaseVariableNamingChecker(Checker):
    class Variable:
        def __init__(self):
            self.line_num = 100000000000000000

    def __init__(self, code):
        self.variables: Dict[str, CamelCaseVariableNamingChecker.Variable] = {}

    def comments(self):
        for name, var in self.variables.items():
            yield Comment(
                var.line_num,
                f"Generally, camel case is not used to name variables in Python. Instead, try to write words in all "
                f"lowercase separated by underscores, e.g. `{snakecase(name)}` rather than `{name}`.",
            )

    def visit_Name(self, node):
        name, context = node.id, node.ctx
        if (
            isinstance(node.ctx, ast.Store)
            and name != name.upper()
            and name != name.lower()
        ):
            if name not in self.variables:
                self.variables[name] = self.Variable()
            var = self.variables[name]
            var.line_num = min(var.line_num, node.lineno)
        self.generic_visit(node)


@question_checker("ThrowerAnt")
class WrongMaxRangeChecker(Checker):
    def __init__(self, code):
        self._comments = []

    def comments(self):
        yield from self._comments

    def visit_Assign(self, node):
        targets, value = node.targets, node.value
        if (
            len(targets) == 1
            and isinstance(targets[0], ast.Name)
            and targets[0].id == "max_range"
            and isinstance(value, ast.Num)
            and value.n < 10000
        ):
            self._comments.append(
                Comment(
                    node.lineno,
                    f"The code uses the magic number {value.n} here as the `max_range` which might cause problems in "
                    f"the future, because if we ever increased the board size, the `ThrowerAnt` would be unable to "
                    f"attack bees further than {value.n} places away. Try using `float('inf')` (infinity) instead.",
                )
            )
        self.generic_visit(node)


@question_checker("ThrowerAnt")
class WrongMaxRangeChecker(Checker):
    def __init__(self, code):
        self._comments = []

    def comments(self):
        yield from self._comments

    def visit_Assign(self, node):
        targets, value = node.targets, node.value
        if (
            len(targets) == 1
            and isinstance(targets[0], ast.Name)
            and targets[0].id == "max_range"
            and isinstance(value, ast.Num)
            and value.n < 10000
        ):
            self._comments.append(
                Comment(
                    node.lineno,
                    f"The code uses the magic number {value.n} here as the `max_range` which might cause problems in "
                    f"the future, because if we ever increased the board size, the `ThrowerAnt` would be unable to "
                    f"attack bees further than {value.n} places away. Try using `float('inf')` (infinity) instead.",
                )
            )
        self.generic_visit(node)


@question_checker("ThrowerAnt")
class HiveEqualityNotIdentityChecker(Checker):
    def __init__(self, code):
        self._comments = []

    def comments(self):
        yield from self._comments

    def visit_Compare(self, node):
        if len(node.ops) == 1:
            left = node.left
            op = node.ops[0]
            right = node.comparators[0]
            if (
                (isinstance(left, ast.Name) and left.id == "hive")
                or (isinstance(right, ast.Name) and right.id == "hive")
            ) and not isinstance(op, ast.IsNot):
                self._comments.append(
                    Comment(
                        node.lineno,
                        "Notice that we pass a `hive` instance directly to this method so we should use "
                        "Python's `is not` here to test identity. The code also works when using `!=` "
                        "but since there's only one specific `hive`, checking for identity here makes a "
                        "little more sense since the `Place` class doesn't define an equality method.",
                    )
                )
        self.generic_visit(node)


@question_checker("ThrowerAnt")
class HiveEqualityNotIdentityChecker(Checker):
    def __init__(self, code):
        self._comments = []

    def comments(self):
        yield from self._comments

    def visit_Str(self, node):
        if node.s == "Hive":
            self._comments.append(
                Comment(
                    node.lineno,
                    "The code should not be checking if the name of the place is 'Hive'. The "
                    "abstraction barrier is being violated! This is why one of the parameters is "
                    "`hive`. This is a pointer to the Hive instance and can be used to check if the "
                    "current place is the hive. So `{place-var-name}.name != 'Hive'` should be "
                    "`{place-var-name} is not hive`.",
                    ["place-var-name"],
                )
            )
        self.generic_visit(node)


@question_checker("Short and LongThrowers")
class RedefinedNearestBeeChecker(Checker):
    def __init__(self, code):
        self._comments = []

    def comments(self):
        yield from self._comments

    def visit_FunctionDef(self, node):
        if node.name == "nearest_bee":
            self._comments.append(
                Comment(
                    node.lineno,
                    f"Instead of repeating all the code for `nearest_bee` for both `ShortThrower` and `LongThrower`, "
                    f"using the regular `ThrowerAnt`'s `nearest_bee` function would reduce the amount of code needed "
                    f"significantly. The point of classes is that you can generalize one function to do the tasks of "
                    f"many functions with minimal code changes.",
                )
            )
        elif node.name == "__init__":
            self._comments.append(
                Comment(
                    node.lineno,
                    f"An `__init__` method that simply calls it's base class's `__init__` is unnecessary because "
                    f"inheritance will do this automatically without this method in `LongThrower` and `ShortThrower`.",
                )
            )
        self.generic_visit(node)


@question_checker("FireAnt")
class NoCallClassReduceArmor(Checker):
    def __init__(self, code):
        self._comments = []

    def comments(self):
        yield from self._comments

    def visit_AugAssign(self, node):
        if isinstance(node.op, ast.Sub):
            if isinstance(node.value, ast.Name) and node.value.id == "amount":
                self._comments.append(
                    Comment(
                        node.lineno,
                        f"The `Ant.reduce_armor` method already takes care of removing an insect if its armor drops to "
                        f"0 or below, so we could take advantage of that by calling `Ant.reduce_armor(self, amount)` "
                        f"rather than duplicating the logic here. In addition, it would allow further modularity if "
                        f"we wanted to modify the `reduce_armor` method; instead of changing the code in many place, "
                        f"changing it in one place may suffice.",
                    )
                )
            else:
                self._comments.append(
                    Comment(
                        node.lineno,
                        f"Consider calling the `Bee.reduce_armour` method rather than trying to manually reimplement "
                        f"it here, since this will duplicate logic already written elsewhere. In addition, it would "
                        f"allow further modularity if we wanted to modify the `reduce_armor` method; instead of "
                        f"changing the code in many place, changing it in one place may suffice.",
                    )
                )
        self.generic_visit(node)


@question_checker("BodyguardAnt - Place")
class ExtraAttributeAccessChecker(Checker):
    def __init__(self, code):
        self._comments = []

    def comments(self):
        yield from self._comments

    def visit_Attribute(self, node):
        if node.attr == "is_container":
            self._comments.append(
                Comment(
                    node.lineno,
                    f"Checking for `insect.is_container` or `self.ant.is_container` is redundant as it is handled by "
                    f"the `can_contain` method.",
                )
            )
        self.generic_visit(node)
