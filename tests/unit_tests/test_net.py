# -*- coding: utf-8 -*-

# The MIT License (MIT) - Copyright (c) Dave Vandenbout.

import pytest

from skidl import Net, NetClass, Part, Pin

from .setup_teardown import setup_function, teardown_function


def test_nets_1():
    """Test basic net operations."""
    gnd = Net("GND")
    a = Net("A")
    b = Net("B")
    c = Net()
    p = Pin()
    assert len(default_circuit.get_nets()) == 0  # No nets initially.
    assert len(a) == 0  # Net 'a' is empty.
    assert len(b) == 0  # Net 'b' is empty.
    assert len(c) == 0  # Net 'c' is empty.
    a += p  # Add pin to net 'a'.
    assert len(default_circuit.get_nets()) == 1  # One net in the circuit.
    assert len(a) == 1  # Net 'a' has one pin.
    assert len(b) == 0  # Net 'b' is still empty.
    assert len(c) == 0  # Net 'c' is still empty.


def test_net_get_pull_1():
    """Test getting and fetching nets."""
    net1 = Net.get("test_net")
    assert net1 is None  # Net 'test_net' does not exist.
    net2 = Net.fetch("test_net")
    assert isinstance(net2, Net)  # Net 'test_net' is created.
    assert len(default_circuit.nets) == 2  # NOCONNECT net is always there.
    net3 = Net.get("test_net")
    assert id(net3) == id(net2)  # Same net object.
    assert len(default_circuit.nets) == 2  # No new net should have been created.


def test_net_fixed_name_1():
    """Test net with fixed name."""
    net_fixed = Net("A", fixed_name=True)
    net_merged = Net()
    net_merged += net_fixed  # Merge fixed name net.
    for _ in range(5):
        net_merged += Net()  # Merge additional nets.
    default_circuit.merge_net_names()
    assert net_merged.name == "A"  # Name should remain 'A'.


def test_netclass_1():
    """Test assigning netclass to a net."""
    led = Part("Device", "LED_ARBG")
    n1 = Net()
    n1 += led[1, 2, 3, 4]  # Add LED pins to net.
    n1.netclass = NetClass("my_net", a=1, b=2, c=3)  # Assign netclass.


def test_netclass_2():
    """Test reassigning netclass to a net."""
    led = Part("Device", "LED_ARBG")
    n1 = Net()
    n1 += led[1, 2, 3, 4]  # Add pins to net.
    n1.netclass = NetClass("my_net", a=1, b=2, c=3)  # Assign netclass.
    with pytest.raises(ValueError):
        n1.netclass = NetClass("my_net", a=5, b=6, c=7)  # Reassign netclass should raise error.


def test_netclass_3():
    """Test merging nets with different netclasses."""
    n1, n2 = Net("a"), Net("b")
    n1.netclass = NetClass("class1")  # Assign netclass to n1.
    n2.netclass = NetClass("class2")  # Assign netclass to n2.
    with pytest.raises(ValueError):
        n1 += n2  # Merging nets with different netclasses should raise error.


def test_netclass_4():
    """Test netclass propagation after merging nets."""
    n1, n2 = Net("a"), Net("b")
    n1 += n2  # Merge nets.
    n1.netclass = NetClass("class1")  # Assign netclass to merged net.
    assert n2.netclass.name == "class1"  # Netclass should propagate.
    with pytest.raises(ValueError):
        n2.netclass = NetClass("class2")  # Reassigning netclass should raise error.


def test_drive_1():
    """Test drive strength propagation after merging nets."""
    n1, n2 = Net("a"), Net("b")
    n1.drive = 5  # Set drive strength.
    n2.drive = 6  # Set different drive strength.
    n1 += n2  # Merge nets.
    assert n1.drive == n2.drive  # Drive strength should be the same.
    assert n1.drive == 6  # Drive strength should be the higher value.


def test_drive_2():
    """Test drive strength update after merging nets."""
    n1, n2 = Net("a"), Net("b")
    n1.drive = 5  # Set drive strength.
    n1 += n2  # Merge nets.
    assert n1.drive == n2.drive  # Drive strength should be the same.
    assert n2.drive == 5  # Drive strength should be 5.
    n1.drive = 7  # Update drive strength.
    assert n2.drive == 7  # Drive strength should be updated.
