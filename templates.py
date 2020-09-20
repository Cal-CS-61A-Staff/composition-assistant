# fmt: off
# noinspection PyDictCreation
import config
proj = config.proj

templates = {
    "noeffect": "This statement has no effect. You should remove it, since it has no effect on your program.",
    "commented-code": "You should remove commented-out code from your final product.",
    "simul-assign": "Python supports simultaneous assignment, which would be cleaner to use here. "
                    "e.g.: `a, b, c = 0, 0, 0`",
    "extra-swap": "Rather than using a temporary variable to swap two variables, you can use simultaneous assignment "
                  "e.g. `{first}, {second} = {second}, {first}`",
    "unnecessary-loop-var": "Nice use of a loop here to keep the logic nice and tidy. But as a convention in Python, "
                            "if the name assigned in each loop is not used, we can call it `_` to denote that it's "
                            "really just a placeholder.",
    "ambiguous-variable": "`{original_var_name}` might be ambiguous. A name like `{alternative}` could help clarify.",
    "nice-inline-comment": "Nice use of in-line comments to clarify your logic.",
    "redundant-code": "Notice that you repeat `{repeated_code}` multiple times in your code, which is redundant. "
                      "Consider rearranging your code to avoid such repetition. {hint}",
    "spacing": "Remember to use spaces around your operators: `x=0` -> `x = 0`",
    "unnecessary-parens": "Parentheses are not necessary in Python conditionals. You can write `if (X):` as `if X:`",
    "call-expensive-function": "Rather than calling `{expensive_function}` multiple times, it is better to store its "
                               "return value and use it whenever it is needed. This avoids redundant and possibly "
                               "expensive function calls.",
    "incorrect-comments": "While comments can make reading code easier, make sure to keep them consistent with what "
                          "your code actually does!",
    "confusing-helper-functions": "Whenever we define a function, as a programmer, we make a decision to include some "
                                  "information and exclude other information. Here, the code hides some of the game "
                                  "behind helper functions. But the names are both shorthand that requires looking at "
                                  "the body of the function to understand. Especially because the functions are very "
                                  "short, we can instead inline the code in the body of the loop. This way, we can "
                                  "provide better context for what the code does than function names alone.",
    "while-instead-of-for-loop": "Could you use a `for` loop with `range` here, instead of a `while` loop?",
    "extra-variable": "Reflect on the variable `{extra-variable}`. Is this variable necessary to keep track of? Is "
                      "there a way to achieve the code’s purpose without using it?",
}

hog_templates = {
    "roll_dice": {
        "roll-results-in-list": "This is a very unique approach, I like how you incorporated lists into this! However, in "
                                "terms of efficiency, you do not need to keep track of every single roll result in a list, "
                                "then search through the list for a `1`; you only need to check if a given roll is a `1` "
                                "in every iteration of the loop. This can be done using a boolean and a single `for` loop! "
                                "Makes it a little easier on memory and runtime.",
        "has-one-flag": "Rather than counting the number of times the dice outcome is 1, the code can have a boolean flag "
                        "that becomes true when a call to `dice()` is 1. The code can then return the total of outcomes or "
                        "1 depending on the boolean flag after the loop.",
        "extra-nested-loop": "Having this nested loop makes the code more complicated than it should be. Instead, the code "
                             "could have a boolean flag that becomes true when a call to `dice()` is 1. At the end, return "
                             "the total of outcomes or 1 depending on the boolean flag after the loop. By keeping the "
                             "behavior similar to both pig out and non pig out cases, the code is greatly simplified.",
    },
    "play": {
        "use-max-function": "Can you use the `max` function to find the correct condition instead of saying "
                            "`score1 < goal` and `score0 < goal`?",
        "two-turns-per-iteration": "The code should not run two turns in one iteration. Instead `player` should be used in "
                                   "an `if` to figure out which segment of code should be run. Then use the `other` "
                                   "function to update the `player` value.",
        "hardcoded-100": "100 should not be hard-coded as the winning value for the scores. The code should be using the "
                         "function parameter `goal`.",
        "multiple-player-comparisons": "The value of `player` can only ever be 0 or 1, therefore instead of two `if`'s "
                                       "this code can be an `if...else` clause instead. "
                                       "Like so: ```if player == 0:\n\t# player 0 stuff\nelse:\n\t# player 1 stuff```",
        "labeled-names": "Nitpick: Since only one of the if clause or the else clause will be entered on each loop "
                         "iteration, there's no need to label all your names with the player number. ",

    },
    "max_scoring_num_rolls": {
        "call-make-averaged-in-loop": "Since `roll_dice` and `num_samples` do not change in the iteration, the code can "
                                      "call `make_averaged(roll_dice, num_samples)` outside of the loop and assign it "
                                      "to a name. Whether it is called outside the loop or within, that name is the "
                                      "same. This avoids repeating redundant and possibly expensive function calls.",
        "hardcoded-num-samples": "The number of samples should not be hardcoded as `1000` here. Instead, the name "
                                 "`num_samples` should be used in case when the function is called a different value is "
                                 "provided.",
    },
}

typing_test_templates = {
    "repeated-return": "Instead of having the same repeated return statement for each if/elif/else case, how can you "
                       "factor it out of the if/elif/else statements to run at the end of your function.",
    "slice-recursion": "Great use of recursion! Something to think about is that your recursive call makes a copy of a "
                       "sliced list every time. However, each time you slice a list, you have to add all the elements "
                       "to a new list. In the future, think about what that means in terms of efficiency. Is there an "
                       "simpler way to do this with iteration instead?",
    "unnecessary-strip": "It is not necessary to call `strip` if you are calling `split` with no other argument.",
    "unnecessary-full": "Because our iteration will compare each of the words inside the shortest list (between the "
                        "original and the typed), it would consider the case in which someone scores full points. Thus "
                        "this base case is unnecessary.",
    "good-min-key": "Nice use of the min function with a key! This makes the code not only efficient, but easy to read "
                    "and understand.",
    "no-min-key": "Consider using `min` with a key, rather than using a for loop.",
    "extra-list": "Generally, if there is a simpler way to solve without creating an extra list or dictionary, this "
                  "way is preferable because it reduces complexity. How could you use min with a key function to help "
                  "here?",
    "deep-lookahead": "Don’t try to look more than one character ahead - let the recursion handle this.",
    "complex-base-case": "Some of your base cases can be simplified - if both words are still nonempty, can you "
                         "continue to recurse?",
    "repeated-key-dist-calls": "Don't call `get_key_distances()` on every function invocation, as it is expensive to "
                               "call - instead, use the provided variable `KEY_DISTANCES`.",
    "use-min": "How can we use the `min` function, rather than a series of if statements, to compute the desired value?",
    # "use-zip": "Consider using `zip` to iterate over two sequences simultaneously.",
    "not-instead-of-empty-comp": "You can use `not` to test if a string is empty, rather than comparing it to the "
                                 "empty string.",
    "extra-index-variable": "Consider iterating through `words_list` directly, rather than introducing an extra "
                            "index variable that is not necessary",
    "duplicated-loops": "Notice that this `for` loop is repeated multiple times in this function in the various "
                        "branches of your conditional. Consider moving it outside the conditional, and compute the "
                        "argument to `range` using `min`!",
    "long-line": "This line is very long! Consider computing some of its subexpressions and storing their values in "
                 "separate variables first, rather than doing everything in the same line.",
    "weird-append": "Rather than appending to an output list, consider computing the wpm and accuracy in separate "
                    "variables, and constructing the output list from the two variables only at the end when you "
                    "return.",
}

cats_templates = {
  "accuracy": {
    "for-loop-with-range": "Could you use a `for` loop with `range` here, instead of a `while` loop? This removes the "
                              "need for an extra index variable ",
    "earlier-length-check": "We should check if `len(typed_words) == 0` before attempting to calculate the score as it "
                              "gives a cleaner flow of logic/makes it obvious that if length is 0, there's no need to "
                              "do any extra work.",
    "if-instead-of-min": "You can use `min`, rather than a series of `if/elif/else` statements, to compute the desired value.",
    "good-min-use": "Nice use of the min function to consolidate code logic of checking lengths into your for loop condition!"
    },
  "autocorrect": {
    "extra-index-variable": "Consider iterating through `valid_words` directly, rather than introducing an extra "
                              "index variable that is not necessary",
    "check-in-list": "A more concise way of checking if a element is contained within a list is to use the `in` operator "
                          "for example, `if elem in lst:` ",
    "redundant-diff-func-call": "Since these calls to `diff_function` use the same parameters, we should store the output "
                              "in a variable to avoid redundant function calls.",
    "good-min-key": "Nice use of the min function with a key! This makes the code not only efficient, but easy to read "
                      "and understand.",
    "use-lambda": "Since this helper function is pretty simple and is just needed for the key of the `min` "
                                "function call, we can write it as a lambda expression instead to make our code more concise. ",
    "good-zip-use": "Great use of the `zip` function!",
    "good-dict-use": "Great use of a dictionary to utilize it's `.get` method as the `key` for the `min` function!",
  },
}

ants_templates = {
    "Short and LongThrowers": {
        "no-min-max-range": "This method is a good start but it does not implement the `min_range` and `max_range` "
                            "checks that it should be. There isn't a need to have additional `nearest_bee` functions "
                            "in the `ShortThrower` and `LongThrower` classes, it's mostly just duplicated code! "
                            "Try to combine your three implementations in one general one here. For starters, it helps "
                            "to define `min_range` and `max_range` in the `ThrowerAnt` class.",
        "confusing-recursive-elif": "Great job doing this recursively! Notice that each of the `elif` statements have "
                                    "the same return value, and the condition statements are all very similar. Think "
                                    "about how the code could compact these into one `if` statement. Also, remember "
                                    "LongThrowers and ShortThrowers are instances of the Thrower Ant, so you can add "
                                    "`min_range` and `max_range` attributes to the `ThrowerAnt` class and override "
                                    "these values in your `LongThrower` and `ShortThrower` classes to make this "
                                    "simpler.",
        "nearest-bee-repeated": "Instead of repeating all the code for `nearest_bee` for both `ShortThrower and "
                                "`LongThrower` thrower, using the regular `ThrowerAnt`'s near_bee function would "
                                "reduce the amount of code needed significantly. The point of classes is that you can "
                                "generalize one function to do the tasks of many functions with minimal code changes.",
        "max-range-attribute": "Nitpick: Notice how we don't have to add max_range as a class attribute because "
                               "it will inherit it from the ThrowerAnt class.",
        "useless-init": "An `__init__` method that simply calls it's base class's `__init__` is unnecessary because "
                        "inheritance will do this automatically without this method in `LongThrower` and "
                        "`ShortThrower`.",
    },
    "ThrowerAnt": {
        "range-bounds-confusing": "Instead of having to check if `min_range` and `max_range` are not properly defined, "
                                  "they could have been set to the extremes of the range like 0 and 99999.",
        "max-range-too-small": "The code uses the magic number {limit} here as the `max_range` which might cause "
                               "problems in the future, because if we ever increased the board size, the `ThrowerAnt` "
                               "would be unable to attack bees further than {limit} places away. Try using "
                               "`float('inf')` (computer representation of infinity) instead.",
        "good-readability": "Great work! Easy to read and intuitive, and I like how this code is general and can be "
                            "reused on any board, and also for subclasses.",
        "good-no-rewrite-nearest-bee": "Great job! I like how you recognized that you didn't have to rewrite "
                                       "`nearest_bee` in this class because it inherits from `ThrowerAnt`!",
        "good-range-bounds": "Nice work! Setting min and max to extremes initially helps make the code more general "
                             "because if we ever increased the board size, the `ThrowerAnt` will be able to attack "
                             "bees for the correct number of places away.",
        "hive-place-name-checking": "The code should not be checking if the name of the place is 'Hive'. The "
                                    "abstraction barrier is being violated! This is why one of the parameters is "
                                    "`hive`. This is a pointer to the Hive instance and can be used to check if the "
                                    "current place is the hive. So `place.name != 'Hive'` should be "
                                    "`place is not hive`.",
        "no-hive-distance-variable": "A good way of figuring out where our position is relative to the ranges is "
                                     "keeping a distance variable. Then, `while place is not hive:`, we can change "
                                     "our current `place` to `place.entrance`, and then increment our distance by "
                                     "1 each time. As long as it's within our `min` and `max ranges`, if `place.bees` "
                                     "has something in it, we can make a call to `random_or_none`.",
        "all-ant-range-attributes": "I noticed that you added `min_range` and `max_range` attributes to the `Ant` "
                                    "class instead of the `ThrowerAnt` class! This works, but since these attributes "
                                    "are only meaningful when we talk about `ThrowerAnt`s, it might be better to move "
                                    "them here; after all, it doesn't make sense for `HarvesterAnt`s to have a range.",
        "multiple-range-cases": "Instead of having multiple cases (`if self.min_range`, `if self.max_range`, `else`), "
                                "we can consolidate the logic into one `while` loop. Try writing something like this:\n"
                                """
```
place = self.place
dist = 0
while place is not hive:
    if self.min_range <= dist <= self.max_range:
    # YOUR CODE HERE
```
""",
        "hive-equality-not-identity": "Notice that we pass a `hive` instance directly to this method so we should use "
                                      "Python's `is not` here to test identity. The code also works when using `!=` "
                                      "but since there's only one specific `hive`, checking for identity here makes a "
                                      "little more sense since the `Place` class doesn't define an equality method.",
        "no-while-loop-place-finder": "A better approach would be to have a `while` loop to get to the proper range of "
                                      "`place`'s (and making sure it doesn't hit the `hive`) and then another `while` "
                                      "loop that goes until it either hits the `hive` or the max range. In the latter "
                                      "loop it checks if the current, within range, place has bees, and if `True` "
                                      "returns a bee.",
        "check-end-none-not-hive": "Rather than checking if the end of the chain of places has been reached `hive` "
                                   "should have been used, since the abstraction barrier is current being broken with "
                                   "the assumption `hive` will not have anything after it.",
        "bad-empty-list-check": "Nitpick: Another way of saying `{bad-list-check}` is simply `{good-check}`. This is "
                                "because the empty list is a false-y value so we don't need the additional `!= []`.",
        "bad-recursion": "Great job doing this recursively! Notice that many of the `elif` statements have similar "
                         "return values, and the condition statements are all very similar. Think about how the code "
                         "could compact these into one `if` statement."
    },
    "FireAnt": {
        "no-call-ant-reduce-armor": "The `Ant.reduce_armor`method already takes care of removing an insect if its "
                                    "armor drops to 0 or below, so we could take advantage of that by calling "
                                    "`Ant.reduce_armor(self, amount)` rather than duplicating the logic here. This "
                                    "would reduce the amount of code needed as we no longer have to manually remove "
                                    "our insect and we can dedicate the rest of this method to the special features of "
                                    "a FireAnt without worrying about the general things all Ants need to do when "
                                    "their armor is reduced. In addition, it would allow further modularity if we "
                                    "wanted to modify the `reduce_armor` method; instead of changing the code in many "
                                    "places, changing it in one place may suffice.",
        "call-insect-reduce-armor": "Calling `Insect.reduce_armor` gives us less room for future customization. It "
                                    "would be better to call `Ant.reduce_armor`. This way, if we were to later "
                                    "modify how `reduce_armor` works for ants, the change would be reflected in the "
                                    "FireAnt class.",
        "reduce-armor-called-after-check": "How about calling `Ant.reduce_armor(self,amount)` before the `if` clause? "
                                           "Then the condition in the `if` clause could simply be `if self.armor <= 0:`"
                                           "which would look nicer. Also, it would better reflect the logic of what is "
                                           "happening. We always reduce the armor of `self`, and then the `if` "
                                           "condition depends on whether or not the ant is still alive.",
        "iterating-over-mutating-list": "If we call `reduce_armor` on a `Bee` object, the pointer to that `Bee` in the "
                                        "`self.place.bees` list will be removed because of how `reduce_armor` was "
                                        "implemented - read the given code carefully to see why . That is why we need "
                                        "to make a copy to iterate through the list; we cannot iterate through it as "
                                        "we mutate it (we'll miss some elements because the indices keep changing).",
        "confusing-iterate-mutating-list": "It seems like this logic is here to handle the fact that we can't mutate a "
                                           "list as we iterate over it. This works, but an easier way to get around "
                                           "this issue is to iterate over a copy of the list. That is, we could say "
                                           "`for bee in list(place.bees):`",
        "iterate-no-use-range": "Instead of getting the number of bees and using a `range` here, the code could "
                                "iterate through the bees themselves: `for bee in list(self.place.bees)`",
        "call-class-method-reduce-armor": "Calling `Insect.reduce_armor(bee, self.damage)` gives us less room for "
                                          "future customization. It would be better to call "
                                          "`bee.reduce_armor(self.damage)`.",
        "comprehension-not-loop": "One small thing is that we generally only want to use list comprehensions when we "
                                  "care about the list that is being created by it. In this case, "
                                  "`[{bee-var-name}.reduce_armor(self.damage) for {bee-var-name} in {bee-list-name}]`"
                                  " creates a list of None's which is unnecessary. Try replacing the list "
                                  "comprehension with a for loop.",
    },
    "BodyguardAnt - Ant": {
        "complex-return-expression": "Good job, but try to simplify this function to just one boolean expression!",
        "extra-if-else": "Remember that this whole conditional itself evaluates to a boolean value! So we can just "
                         "return the expression without using `if ... else...`."
    },
    "BodyguardAnt - Place": {
        "no-use-can-contain": "We should use the `can_contain` function here to check for a valid container ant "
                              "copying code. There is no point in letting functions we've already written go to waste!",
        "no-use-contain-ant": "The code should use the `contain_ant` method here to maintain abstraction barriers.",
        "extra-checks": "Checking for `insect.is_container` or `self.ant.is_container` is redundant as it is handled "
                        "by the the `can_contain` method.",
    },
}

# fmt: on

templates["custom"] = None

#TODO: update **<proj>_templates to match project
temp = {
  "ants": ants_templates,
  "cats":cats_templates,
  "type":typing_test_templates,
  "hog":hog_templates
}

templates_by_problem = {"common": templates, **temp[proj]}

templates = {
    key: template
    for problem in templates_by_problem.values()
    for key, template in problem.items()
}


def template_completer(name):
    relevant_keys = list(templates_by_problem[name]) + list(
        templates_by_problem["common"]
    )

    def completer(text, state):
        cnt = 0
        out = set()

        for key in relevant_keys:
            if key in out:
                continue
            if key.startswith(text.strip()):
                if cnt == state:
                    return key
                out.add(key)
                cnt += 1

        if out:
            return

        for key in relevant_keys:
            if key in out:
                continue
            for word in text.split("-"):
                if word and word in key.split("-"):
                    if cnt == state:
                        return key
                    out.add(key)
                    cnt += 1
                    break

        return None

    return completer
