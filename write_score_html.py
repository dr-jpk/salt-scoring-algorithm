# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:47:07 2015

@author: jpk

This script writes the nighly block score for P0, P1, P2 and P3 targets in html
to be displayed on the web.
"""

import pandas as pd
import MySQLdb
import os
import HTML as html

def get_block_scores(mysql_cons):

    query = pd.read_sql('''SELECT Proposal_Code,
    Block_Id,
    VisibilityStart as T_start,
    VisibilityEnd as T_end,
    Priority as P,
    getProposalTotal_time(Block_Id) AS tTime,
    getProposalUsed_time(Block_Id) AS usedTime,
    round(getBlockFraction(Block_Id),3) AS BF,
    round(getProposalCompleteness(Block_Id),3) AS PC,
    round(getBlockCompleteness(Block_Id), 3) AS BC,
    getObjectAvailability(Block_Id) AS Dleft,
    getDaysAvailable(Block_Id) AS DaysAvail,
    round(get_w_P_score(Block_Id),3) AS wP_score,
    round(get_w_PR_score(Block_Id),3) AS wPR_score,
    round(get_w_BF_score(Block_Id),3) AS wBF_score,
    round(get_w_PC_score(Block_Id),3) AS wPC_score,
    round(get_w_BC_score(Block_Id),3) AS wBC_score,
    round(get_w_OA_score(Block_Id),3) AS wOA_score,
    round( get_w_Tot_score(Block_Id),3) AS wTot_score
    FROM V_BlockTonight_VisWin
    JOIN Block USING (Block_Id)
    WHERE Priority < 4 ORDER BY wTot_score DESC;
    ''', con=mysql_con)

    return query

if __name__=='__main__':

    # open mysql connection to the sdb
#    mysql_con = MySQLdb.connect(host=os.environ['SDBHOST'],
#                                port=3306, user=os.environ['SDBUSER'],
#                                passwd=os.environ['SDBPASS'],
#                                db='sdb')

    # open mysql connection to the sdb TESTING:
    mysql_con = MySQLdb.connect(host='devsdb.cape.saao.ac.za',
                                port=3306, user='jpk',
                                passwd='thankserc',
                                db='sdb_v6')

    blocks = get_block_scores(mysql_con)

    with open('BlocksTonight.html', 'w') as out:
        out.write(blocks.to_html(col_space=20,
                                 formatters={https://www.salt.ac.za/wm/proposal/2014-2-SCI-035#block32259}))
