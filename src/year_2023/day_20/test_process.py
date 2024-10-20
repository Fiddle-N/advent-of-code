from year_2023.day_20 import process


def test_mod_config_1_pulse_history():
    mod_config = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
    pulse_runner = process.PulseRunner(mod_config)
    assert next(pulse_runner) == [
        process.PulseMsg(pulse=process.Pulse.LOW, source='button', dest='broadcaster'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='broadcaster', dest='a'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='broadcaster', dest='b'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='broadcaster', dest='c'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='a', dest='b'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='b', dest='c'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='c', dest='inv'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='inv', dest='a'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='a', dest='b'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='b', dest='c'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='c', dest='inv'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='inv', dest='a'),
    ]


def test_mod_config_1_pulses_after_1000_btn_presses():
    mod_config = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
    pulse_runner = process.PulseRunner(mod_config)
    for _ in range(1000):
        next(pulse_runner)
    assert pulse_runner.low_pulses == 8000
    assert pulse_runner.high_pulses == 4000
    assert pulse_runner.low_pulses * pulse_runner.high_pulses == 32000000


def test_mod_config_2_pulse_history():
    mod_config = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
    pulse_runner = process.PulseRunner(mod_config)
    assert next(pulse_runner) == [
        process.PulseMsg(pulse=process.Pulse.LOW, source='button', dest='broadcaster'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='broadcaster', dest='a'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='a', dest='inv'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='a', dest='con'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='inv', dest='b'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='con', dest='output'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='b', dest='con'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='con', dest='output'),
    ]
    assert next(pulse_runner) == [
        process.PulseMsg(pulse=process.Pulse.LOW, source='button', dest='broadcaster'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='broadcaster', dest='a'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='a', dest='inv'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='a', dest='con'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='inv', dest='b'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='con', dest='output'),
    ]
    assert next(pulse_runner) == [
        process.PulseMsg(pulse=process.Pulse.LOW, source='button', dest='broadcaster'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='broadcaster', dest='a'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='a', dest='inv'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='a', dest='con'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='inv', dest='b'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='con', dest='output'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='b', dest='con'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='con', dest='output'),
    ]
    assert next(pulse_runner) == [
        process.PulseMsg(pulse=process.Pulse.LOW, source='button', dest='broadcaster'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='broadcaster', dest='a'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='a', dest='inv'),
        process.PulseMsg(pulse=process.Pulse.LOW, source='a', dest='con'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='inv', dest='b'),
        process.PulseMsg(pulse=process.Pulse.HIGH, source='con', dest='output'),
    ]


def test_mod_config_2_pulses_after_1000_btn_presses():
    mod_config = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
    pulse_runner = process.PulseRunner(mod_config)
    for _ in range(1000):
        next(pulse_runner)
    assert pulse_runner.low_pulses == 4250
    assert pulse_runner.high_pulses == 2750
    assert pulse_runner.low_pulses * pulse_runner.high_pulses == 11687500
