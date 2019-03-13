"""
For when user double clicks on any medical treeview
"""
from modules.othermodules.sqlitefunctions import AdvDbQuery
from modules.othermodules.globals import Globals
from modules.othermodules.popup import PopUpWindow


def medical_popup(master, tree, event=None):

    # Make sure heading not selected before continuing.
    # ========
    region = tree.identify("region", event.x, event.y)
    if region == "heading":
        return

    med_id = tree.item(tree.focus())['values'][0]   # Get selected medical ID

    # Get the relevant entry from the database and build up the string
    # ========
    sql_query = """
        SELECT * FROM Main_Page_Med_history WHERE ID = :ID
        """
    sql_dict = {'ID': med_id}

    results = AdvDbQuery(Globals.conn, sql_query, sql_dict)
    print(results)

    results_string = ""
    for index, value in enumerate(results[0]):
        results_string += str(results[0][index]) + "  :  "
        results_string += str(results[1][0][index]) + "\n"
    print(results_string)

    # Build the medical window:
    # ========
    popup = PopUpWindow(tk.Toplevel(master.master),
                        heading="Medical Entry",
                        text=results_string,
                        main_win = master)
