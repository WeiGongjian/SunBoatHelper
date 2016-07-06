from base import tools
from state import state
from base import button


def supply(kan_num_list,suppy_type="all"):
    for kan_num in kan_num_list:
        assert kan_num in [1,2,3,4]
    if suppy_type=="all":
        state.wait_for_state("home")
        button.get_button("home_supply").click()
        state.wait_for_state("supply","supply_over")
        if 1 in kan_num_list:
            button.get_button("supply_all").click()
        for kan_num in kan_num_list:
            assert kan_num in [2,3,4]
            button.get_button("supply_kan%s" % str(kan_num)).click()
            while state.get_state() == "supply_need":
                button.get_button("supply_kan%s" % str(kan_num)).click()
                button.get_button("supply_all").click()
        button.get_button("home").click()
    
if __name__ == "__main__":
    supply([3])