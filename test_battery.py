import pytest
from battery import Battery
from unittest.mock import Mock

@pytest.fixture
def charged_battery():
    return Battery(100)

@pytest.fixture
def partially_charged_battery():
    b = Battery(100)
    b.mCharge = 70
    return b

def describe_battery():

    def it_sets_correct_values_when_creating_constructor():
        battery = Battery(150)
        assert battery.mCapacity == 150
        assert battery.mCharge == 150
    
    def it_returns_correct_capacity():
        battery = Battery(150)
        assert battery.getCapacity() == 150
    
    def it_returns_correct_initial_charge():
        battery = Battery(200)
        assert battery.getCharge() == 200

    def it_calls_monitor_on_recharge(partially_charged_battery):
        # setup
        mock_monitor = Mock()
        battery = partially_charged_battery # use the fixture
        battery.external_monitor = mock_monitor

        # execute
        battery.recharge(20)   # battery starts at 70, add 20

        # validate
        mock_monitor.notify_recharge.assert_called_once_with(90)

    #put more test cases here.

    def it_calls_monitor_on_drain(charged_battery):
        mock_monitor = Mock()
        battery = charged_battery
        battery.external_monitor = mock_monitor
        battery.drain(30)  # battery starts at 100, drain 30
        mock_monitor.notify_drain.assert_called_once_with(70)
    
    def it_does_not_overcharge(partially_charged_battery):

        mock_monitor = Mock()
        battery = partially_charged_battery
        battery.external_monitor = mock_monitor
        result = battery.recharge(50)
        assert result is True
        assert battery.getCharge() == 100 
        mock_monitor.notify_recharge.assert_called_once_with(100)
    
    def it_does_not_overdrain(charged_battery):
        mock_monitor = Mock()
        battery = charged_battery
        battery.external_monitor = mock_monitor
        result = battery.drain(150)
        assert result is True
        assert battery.getCharge() == 0 
        mock_monitor.notify_drain.assert_called_once_with(0)
    
    def it_fails_to_recharge_when_full(charged_battery):
        mock_monitor = Mock()
        battery = charged_battery
        battery.external_monitor = mock_monitor
        result = battery.recharge(10)
        assert result is False
        assert battery.getCharge() == 100
        mock_monitor.notify_recharge.assert_not_called()
    
    def it_fails_to_drain_when_empty():
        mock_monitor = Mock()
        battery = Battery(100)
        battery.mCharge = 0
        battery.external_monitor = mock_monitor
        result = battery.drain(10)
        assert result is False
        assert battery.getCharge() == 0
        mock_monitor.notify_drain.assert_not_called()

    # State-only tests (no monitor, just verify state changes)
    
    def it_increases_charge_on_recharge_without_monitor(partially_charged_battery):
        # No monitor - test state change only
        result = partially_charged_battery.recharge(20)
        assert result is True
        assert partially_charged_battery.getCharge() == 90
    
    def it_decreases_charge_on_drain_without_monitor(charged_battery):
        # No monitor - test state change only
        result = charged_battery.drain(30)
        assert result is True
        assert charged_battery.getCharge() == 70
    
    def it_fails_to_recharge_with_zero_amount(partially_charged_battery):
        result = partially_charged_battery.recharge(0)
        assert result is False
        assert partially_charged_battery.getCharge() == 70
    
    def it_fails_to_recharge_with_negative_amount(partially_charged_battery):
        result = partially_charged_battery.recharge(-10)
        assert result is False
        assert partially_charged_battery.getCharge() == 70
    
    def it_fails_to_drain_with_zero_amount(charged_battery):
        result = charged_battery.drain(0)
        assert result is False
        assert charged_battery.getCharge() == 100
    
    def it_fails_to_drain_with_negative_amount(charged_battery):
        result = charged_battery.drain(-10)
        assert result is False
        assert charged_battery.getCharge() == 100
    
    def it_caps_charge_at_capacity_without_monitor(partially_charged_battery):
        result = partially_charged_battery.recharge(50)  # 70 + 50 = 120, but cap at 100
        assert result is True
        assert partially_charged_battery.getCharge() == 100
    
    def it_caps_charge_at_zero_without_monitor(charged_battery):
        result = charged_battery.drain(150)  # 100 - 150 = -50, but cap at 0
        assert result is True
        assert charged_battery.getCharge() == 0
    
    def it_preserves_capacity_after_operations(charged_battery):
        charged_battery.drain(50)
        assert charged_battery.getCapacity() == 100
        charged_battery.recharge(25)
        assert charged_battery.getCapacity() == 100
    
    def it_handles_multiple_operations_correctly():
        battery = Battery(100)
        battery.drain(40)
        assert battery.getCharge() == 60
        battery.recharge(20)
        assert battery.getCharge() == 80
        battery.drain(30)
        assert battery.getCharge() == 50
    
    def it_fails_to_recharge_when_full_without_monitor(charged_battery):
        result = charged_battery.recharge(10)
        assert result is False
        assert charged_battery.getCharge() == 100
    
    def it_fails_to_drain_when_empty_without_monitor():
        battery = Battery(100)
        battery.mCharge = 0
        result = battery.drain(10)
        assert result is False
        assert battery.getCharge() == 0
        


