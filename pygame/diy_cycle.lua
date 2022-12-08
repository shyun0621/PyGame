--[[
Diy Cycle
]]

return function(personality_data)
	return wash_step.sequence({
		steps = {
			wash_step.lid.lock(),
			wash_step.pause({ seconds = 5 }),
			wash_step.sub_cycle_update({ sub_cycle = 'fill' }),
			wash_step.fill({
				options = {
					deep_fill_can_change_fill_target_during_this_fill = false
				},
				tumble_profile = false,
				amount = {
					type = 'target_volume',
					data = {
						gallons = 1
					}
				},
				temperature = {
					type = 'active_valve',
					data = {
						valves = { 'primary_cold' }
					}
				}
			}),
			wash_step.pause({ seconds = 10 }),
			wash_step.sub_cycle_update({sub_cycle = 'wash'}),
			wash_step.tumble({
				adaptive_fill_config = false,
				deep_fill_can_change_fill_target_during_this_fill = false,
				time_seconds = 4,
				profile = drive_step.tumble({
					drive_profile_name = 'gfl_tumble_example',
					entries = {
						{ ramp_rate_rpm_per_second = 45, target_speed_rpm = 45, on_time_in_msec = 12000, off_time_in_msec = 5000, direction = 'ccw' },
						{ ramp_rate_rpm_per_second = 45, target_speed_rpm = 45, on_time_in_msec = 12000, off_time_in_msec = 4000, direction = 'cw' }
					}
				})
			}),
			wash_step.sub_cycle_update({ sub_cycle = 'rinse' }),
			wash_step.pause({ seconds = 2 }),
			wash_step.sub_cycle_update({sub_cycle = 'spin'}),
			wash_step.pause({seconds = 10}),
			wash_step.spin({
				recovery = false,
				times = wash_step.spin.level_timed({
					no_spin_seconds = 4,
					normal_seconds = 4,
					more_seconds = 4,
					extra_seconds = 4
				}),
				profile = import(data/global_front_load/wash_steps/spin/profile/closed_loop/spin_drain_test/final_spin_drain_on_test.lua)(personality_data)
			}),
			wash_step.drain_pump_timed({ seconds = 10 }),
			wash_step.lid.unlock()	
		}
	})
end