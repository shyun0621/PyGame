import json


def LoadFromJson(json_file_name):
    with open(json_file_name, 'rb') as f:
        return json.load(f)


def add_spininfo(personal_data_path, time_sec=0):
    temp_str = ""
    temp_str += "\t\t\twash_step.spin({\n"
    temp_str += "\t\t\t\trecovery = false,\n"
    temp_str += "\t\t\t\ttimes = wash_step.spin.level_timed({\n"
    temp_str += "\t\t\t\t\tno_spin_seconds = {},\n".format(time_sec)
    temp_str += "\t\t\t\t\tnormal_seconds = {},\n".format(time_sec)
    temp_str += "\t\t\t\t\tmore_seconds = {},\n".format(time_sec)
    temp_str += "\t\t\t\t\textra_seconds = {}\n".format(time_sec)
    temp_str += "\t\t\t\t}),\n"
    temp_str += "\t\t\t\tprofile = import({})(personality_data)\n".format(personal_data_path)
    temp_str += "\t\t\t}),\n"

    return temp_str


def add_tumbleinfo(time_sec=0):
    temp_str = ""
    temp_str += "\t\t\twash_step.tumble({\n"
    temp_str += "\t\t\t\tadaptive_fill_config = false,\n"
    temp_str += "\t\t\t\tdeep_fill_can_change_fill_target_during_this_fill = false,\n"
    temp_str += "\t\t\t\ttime_seconds = {},\n".format(time_sec)
    temp_str += "\t\t\t\tprofile = drive_step.tumble({\n"
    temp_str += "\t\t\t\t\tdrive_profile_name = 'gfl_tumble_example',\n"
    temp_str += "\t\t\t\t\tentries = {\n"
    temp_str += "\t\t\t\t\t\t{ ramp_rate_rpm_per_second = 45, target_speed_rpm = 45, on_time_in_msec = 12000, off_time_in_msec = 5000, direction = 'ccw' },\n"
    temp_str += "\t\t\t\t\t\t{ ramp_rate_rpm_per_second = 45, target_speed_rpm = 45, on_time_in_msec = 12000, off_time_in_msec = 4000, direction = 'cw' }\n"
    temp_str += "\t\t\t\t\t}\n"
    temp_str += "\t\t\t\t})\n"
    temp_str += "\t\t\t}),\n"

    return temp_str


def add_fillinfo(value):
    temp_str = ""
    temp_str += "\t\t\twash_step.fill({\n"
    temp_str += "\t\t\t\toptions = {\n"
    temp_str += "\t\t\t\t\tdeep_fill_can_change_fill_target_during_this_fill = false\n"
    temp_str += "\t\t\t\t},\n"
    temp_str += "\t\t\t\ttumble_profile = false,\n"
    temp_str += "\t\t\t\tamount = {\n"
    temp_str += "\t\t\t\t\ttype = 'target_volume',\n"
    temp_str += "\t\t\t\t\tdata = {\n"
    temp_str += "\t\t\t\t\t\tgallons = {}\n".format(value)
    temp_str += "\t\t\t\t\t}\n"
    temp_str += "\t\t\t\t},\n"
    temp_str += "\t\t\t\ttemperature = {\n"
    temp_str += "\t\t\t\t\ttype = 'active_valve',\n"
    temp_str += "\t\t\t\t\tdata = {\n"
    temp_str += "\t\t\t\t\t\tvalves = { 'primary_cold' }\n"
    temp_str += "\t\t\t\t\t}\n"
    temp_str += "\t\t\t\t}\n"
    temp_str += "\t\t\t}),\n"

    return temp_str

def add_washcyle():
    temp_str = ""

    temp_str += "\t\t\twash_step.lid.lock(),\n"
    temp_str += "\t\t\twash_step.pause({ seconds = 5 }),\n"
    temp_str += "\t\t\twash_step.sub_cycle_update({ sub_cycle = 'fill' }),\n"
    temp_str += add_fillinfo(2)

    temp_str += "\t\t\twash_step.pause({ seconds = 10 }),\n"
    temp_str += "\t\t\twash_step.sub_cycle_update({sub_cycle = 'wash'}),\n"
    temp_str += add_tumbleinfo(time_sec=90)

    temp_str += "\t\t\twash_step.sub_cycle_update({ sub_cycle = 'rinse' }),\n"
    temp_str += "\t\t\twash_step.pause({ seconds = 10 }),\n"
    temp_str += "\t\t\twash_step.sub_cycle_update({sub_cycle = 'spin'}),\n"
    temp_str += "\t\t\twash_step.pause({seconds = 10}),\n"

    temp_str += add_spininfo(personal_data_path='data/global_front_load/wash_steps/spin/profile/closed_loop/spin_drain_test/final_spin_drain_on_test.lua', time_sec=60)
    temp_str += "\t\t\twash_step.drain_pump_timed({ seconds = 10 }),\n"
    temp_str += "\t\t\twash_step.lid.unlock()"

    return temp_str


def SaveToLua(data, lua_file_name, note=''):
    lua_str = "--[[\n{}\n]]\n\nreturn ".format(note)
    lua_str += "function(personality_data)\n"
    lua_str += "\treturn wash_step.sequence("
    lua_str += "{\n"
    with open(lua_file_name, 'wb') as f:
        lua_str += "\t\tsteps = {\n"
        lua_str += add_washcyle()
        lua_str += "\t\n"
        lua_str += "\t\t}\n"
        lua_str += "\t})\n"
        lua_str += "end"
        f.write(lua_str.encode("utf-8"))


def PasrseJsonToLua(json_file_name, lua_file_name, note=''):
    SaveToLua(LoadFromJson(json_file_name), lua_file_name, note)


def TestJson2Lua(json_file_name, lua_file_name, note=''):
    PasrseJsonToLua(json_file_name, lua_file_name, note)


def TestData2Lua(data, lua_file_name, note=''):
    SaveToLua(data, lua_file_name, note)


if __name__ == "__main__":
    TestJson2Lua("short_sub_cycle_update_test.json", "diy_cycle.lua", "Diy Cycle")
