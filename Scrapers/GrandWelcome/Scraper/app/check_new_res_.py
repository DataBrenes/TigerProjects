import duckdb
def checkNewRes(res_df):
    # create gwdb
    gw_con = duckdb.connect(database='database/grandwelcome.db', read_only=False) 
    gw_con.execute("CREATE TABLE online AS SELECT * FROM res_df")
    new=gw_con.execute("Select * from online where Res_ID NOT IN (Select Res_ID from gw_res)").df()   
    gw_con.execute("drop table IF EXISTS online")
    if len(new) > 0:
        logging.info("Updating Master Database")
        # create relation for adding to db. 
        addnew = gw_con.df(new)
        # add new to database 
        addnew.insert_into("gw_res")    
    gw_con.close()
    return new