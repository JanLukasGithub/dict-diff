from dictionary_diff.diff import *
from dictionary_diff.change import _Remove

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
            "value3.1", "value3.2", "value3.3", "value3.4"
        ]
    },
    "new": {
        "key1": "newvalue1",
        "key2": {
            "key2.1": "newvalue2.1",
            "key2.2": "value2.2"
        },
        "key3": [
            "value3.1", "value3.2", "value3.3", "value3.5"
        ]
    },
    "diff": {
        "key1": "newvalue1",
        "key2": {
            "key2.1": "newvalue2.1"
        },
        "key3": [
            "value3.5", _Remove("value3.4")
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
}, {
    "orig": {
        "key1": "value1",
        "key2": "value2",
        "key3": {
            "key4": "value4",
            "key5": "value5"
        }
    },
    "new": {
        "key2": "value2",
        "key3": {
            "key5": "value5"
        }
    },
    "diff": {
        "key1": _Remove("value1"),
        "key3": {
            "key4": _Remove("value4")
        }
    }
}, {
    "orig": {
        "key1": [
            {"key2": "value2"}, {"key3": "value3"}, {"key4": "value4"}, 1, 2
        ]
    },
    "new": {
        "key1": [
            {"key2": "value20"}, {"key4": "value4"}, {"key3": "value3"}, 3, 2
        ]
    },
    "diff": {
        "key1": [
            {"key2": "value20"}, _Remove({"key2": "value2"}), _Remove(1), 3
        ]
    }
}]

def test_diff():
    for test in test_cases:
        assert equivalent(test["diff"], diff(test["orig"], test["new"]))

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
