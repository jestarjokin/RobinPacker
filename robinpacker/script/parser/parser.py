import robinpacker.script.parser.grammar as grammar

def parse_file(file_name):
    result = grammar.root.parseFile(file_name)
    assert len(result) <= 1
    # TODO: return a RootNode with no rules instead of None
    return result[0] if len(result) else None

def parse_string(rules_string):
    result = grammar.root.parseString(rules_string)
    assert len(result) <= 1
    # TODO: return a RootNode with no rules instead of None
    return result[0] if len(result) else None
