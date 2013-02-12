#! /usr/bin/python

(ARG_TYPE_IMMEDIATE_VALUE, ARG_TYPE_COMPARE_OPERATION, ARG_TYPE_COMPUTE_OPERATION,
 ARG_TYPE_GET_VALUE_1, ARG_TYPE_GET_POS_FROM_SCRIPT) = range(5)


class RootNode(object):
    def __init__(self):
        self.rules = []

    def __repr__(self):
        return "RootNode({})".format(self.rules)


class RuleNode(object):
    def __init__(self):
        self.name = None
        self.conditions = []
        self.actions = []

    def __repr__(self):
        return "RuleNode('{}', {}, {})".format(self.name, self.conditions, self.actions)


class ConditionalNode(object):
    def __init__(self):
        self.negated = False
        self.function = None

    def __repr__(self):
        return "ConditionalNode({}, {})".format(self.negated, self.function)


class FunctionNode(object):
    def __init__(self):
        self.opcode = None
        self.arguments = []

    def __repr__(self):
        return "FunctionNode('{}', {})".format(self.opcode.opName if self.opcode else None, self.arguments)


class ArgumentNode(object):
    def __init__(self):
        self.arg_type = None
        self.value = None

    def __repr__(self):
        return "ArgumentNode({}, {})".format(self.arg_type, self.value)
