from dict_diff import *

test_cases = [{
    "orig": {
        "key1": "value1",
        "key2": {
            "key2.1": "value2.1"
        },
        "key3": [
            "value3.1", "value3.2", "value3.3"
        ]
    },
    "new": {
        "key1": "value1",
        "key2": {
            "key2.1": "value2.1"
        },
        "key3": [
            "value3.1", "value3.2", "value3.3"
        ]
    },
    "diff": {}
}, {
    "orig": {
        "key1": "value1",
        "key2": {
            "key2.1": "value2.1",
            "key2.2": "value2.2"
        },
        "key3": [
            "value3.1", "value3.2", "value3.3"
        ]
    },
    "new": {
        "key1": "newvalue1",
        "key2": {
            "key2.1": "newvalue2.1",
            "key2.2": "value2.2"
        },
        "key3": [
            "value3.1", "value3.2", "value3.3", "value3.4"
        ]
    },
    "diff": {
        "key1": "newvalue1",
        "key2": {
            "key2.1": "newvalue2.1"
        },
        "key3": [
            "value3.1", "value3.2", "value3.3", "value3.4"
        ]
    }
}, {
    "orig": {
        "key1": "value1",
        "key2": {
            "key2.1": "value2.1",
            "key2.2": "value2.2"
        },
        "key3": [
            "value3.1", "value3.2", "value3.3"
        ]
    },
    "new": {
        "key1": 1234,
        "key2": {
            "key2.1": "value2.1",
            "key2.2": True
        },
        "key3": [
            "value3.3", "value3.1", "value3.2"
        ]
    },
    "diff": {
        "key1": 1234,
        "key2": {
            "key2.2": True
        },
    }
}, {
    "orig": {
        "key1": "value1"
    },
    "new": {
        "key1": "value1",
        "key2": "value2"
    },
    "diff": {
        "key2": "value2"
    }
}]

def test_dict_diff():
    for test in test_cases:
        assert equivalent(test["diff"], dict_diff(test["orig"], test["new"], removing=False))
        assert equivalent(test["diff"], dict_diff(test["orig"], test["new"], removing=True))

def test_apply_diff():
    for test in test_cases:
        assert equivalent(test["new"], apply_diff(test["orig"], test["diff"]))

def test_equivalent():
    assert not equivalent(1, "1")
    assert not equivalent(1, True)
    assert not equivalent(True, "1")

    assert equivalent(1, 1)
    assert equivalent("", "")
    assert equivalent(True, True)

    assert equivalent(["value1", "value2", "value3"],
        ["value2", "value3", "value1"])
    assert equivalent([{"key2.1": "value2.1"}, {"key2.2": "value2.2"}, {"key2.3": ["value2.4", "value2.3"]}],
        [{"key2.3": ["value2.3", "value2.4"]}, {"key2.1": "value2.1"}, {"key2.2": "value2.2"}])

    assert equivalent({}, {})
    assert equivalent({"foo": "valuefoo", "bar": "valuebar"},
        {"bar": "valuebar", "foo": "valuefoo"})
    assert not equivalent({"nested": {"key2": "value2"}, "key1": "value1"},
        {"nested": {"key3": "value3"}, "key1": "value1"})
    assert equivalent({"list1": ["value1", "value2", "value3"], "list2": [{"key2.1": "value2.1"}, {"key2.2": "value2.2"}, {"key2.3": ["value2.4", "value2.3"]}]},
        {"list1": ["value2", "value3", "value1"], "list2": [{"key2.3": ["value2.3", "value2.4"]}, {"key2.1": "value2.1"}, {"key2.2": "value2.2"}]})
