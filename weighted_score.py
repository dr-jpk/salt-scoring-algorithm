# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 15:00:44 2014

@author: jpk

a test program to determine the algorith for the queue block scoring

"""

import numpy as np
import matplotlib.pyplot as pl
import MySQLdb as ml
import sys

def P_score(priority):
    '''
    the relative priority weighting is already built in
    '''

    if priority == 0:
        p = 5
    elif priority == 1:
        p = 3
    elif priority == 2:
        p = 2
    elif priority == 3:
        p = 1
    elif priority == 4:
        p = -1

    return p

def PC_score(program_completion):

    pc = 1.03**(program_completion - 60) - 0.15

    return pc

def TC_score(target_completion):

    tc = 0.02 * target_completion

    return tc

def OA_score(object_availability):

    oa = 0.85**object_availability * 4.0

    return oa

def PR_score(PI_ranking):
    if PI_ranking == 1:
        pr = 0.3
    elif PI_ranking == 2:
        pr = 0.2
    elif PI_ranking == 3:
        pr = 0.1

    return pr




def get_Block_data(option='f'):

    if option == 'f':
        blocks = np.load('blocks.npy')
        return blocks
    else:
        pass


    # make the mysql connection
    conn = ml.connect(host = "devsdb.cape.saao.ac.za",user = "jpk",passwd = "thankserc",db = "sdb_v6")
    cursor = conn.cursor()

    query = '''select Proposal_Code,
Block_Id,
Priority,
getPR_score(Block_Id),
round(getBlockFraction(Block_Id),3) as BF,
round(getProposalCompleteness(Block_Id),3) as PC,
round(getBlockCompleteness(Block_Id), 3) as BC,
getDaysAvailable(Block_Id) as DaysAvail,
round(getP_score(Block_Id),6) as P,
round(getPR_score(Block_Id),3) as PR,
round(getBF_score(Block_Id),6) as BF,
round(getPC_score(Block_Id),6) as PC,
round(getBC_score(Block_Id),6) as BC,
round(getOA_score(Block_Id),6) as OA,
round(get_w_P_score(Block_Id),6) as wP,
round(get_w_PR_score(Block_Id),3) as wPR,
round(get_w_BF_score(Block_Id),6) as wBF,
round(get_w_PC_score(Block_Id),6) as wPC,
round(get_w_BC_score(Block_Id),6) as wBC,
round(get_w_OA_score(Block_Id),6) as wOA, 0, 0
from BlockTonight JOIN Block USING (Block_Id);
'''
    cursor.execute(query)

    block_info = cursor.fetchall()

    blocks = np.array(list(block_info),dtype=[('propid','S14'),
                        ('blockid','S10'),
                        ('priority','i4'),
                        ('pi_ranking', 'i4'),
                        ('block_frac', 'f4'),
                        ('completeness', 'f4'),
                        ('block_comp', 'f4'),
                        ('obj_avail', 'f4'),
                        ('p_score','i4'),
                        ('pr_score', 'i4'),
                        ('bf_score', 'f4'),
                        ('pc_score', 'f4'),
                        ('bc_score', 'f4'),
                        ('oa_score', 'f4'),
                        ('wp_score','i4'),
                        ('wpr_score', 'i4'),
                        ('wbf_score', 'f4'),
                        ('wpc_score', 'f4'),
                        ('wbc_score', 'f4'),
                        ('woa_score', 'f4'),
                        ('tot_score', 'f4'),
                        ('wtot_score', 'f4')])

    # close the mysql connection
    cursor.close()
    conn.close()

    return blocks



# TESTING THE CODE AND MAKING PLOTS
if __name__=='__main__':

    # get the blocks data from the test database
    # reading the file from a npy array

    option = 'f' # if q, run a query, if f, run from the saved .npy file

    if option == 'q':
        blocks = get_Block_data('q')
        np.save('blocks', blocks)
    else:
        blocks = get_Block_data('f')

    # print some stats on the returned array
#    print 'No Blocks: ' len(Blocks)
#    print '
#    print

    # weights for each of the scores
    p_w = 1
    pr_w = 1
    bf_w = 1
    pc_w = 1
    bc_w = 1
    oa_w = 0.5

    # this is for testing, override the weighted scores from the mysql query
    # determine the weighted score for each parameter

    blocks['wp_score'] = p_w * blocks['p_score']
    blocks['wpr_score'] = pr_w * blocks['pr_score']
    blocks['wbf_score'] = bf_w * blocks['bf_score']
    blocks['wpc_score'] = pc_w * blocks['pc_score']
    blocks['wbc_score'] = bc_w * blocks['bc_score']
    blocks['woa_score'] = oa_w * blocks['oa_score']

    # determine the unweighted total score for each block
    blocks['tot_score'] = blocks['p_score'] + \
                          blocks['pr_score'] + \
                          blocks['bf_score'] + \
                          blocks['pc_score'] + \
                          blocks['bc_score'] + \
                          blocks['oa_score']

    # determine the weighted total score for each block
    blocks['wtot_score'] = blocks['wp_score'] + \
                           blocks['wpr_score'] + \
                           blocks['wbf_score'] + \
                           blocks['wpc_score'] + \
                           blocks['wbc_score'] + \
                           blocks['woa_score']


    sorted_score = np.argsort(blocks['wtot_score'])

    blocks = blocks[sorted_score]

    # params for plotting
    amount_of_blocks = 100
    frac, no_plots = np.modf(len(blocks) / float(amount_of_blocks))

    if frac == 0.0:
        pass
    else:
        no_plots = no_plots + 1

#    sys.exit(0)

    for i in range(0, int(no_plots)):

        test = blocks[(i*amount_of_blocks):((i+1)*amount_of_blocks)]

        width = 0.45
        ind = np.arange(len(test))
        '''
for i,m in enumerate(maps):
    ax = plt.subplot(nmaps, 1, i+1)
    plt.axis("off")
    plt.imshow(a, aspect='auto', cmap=plt.get_cmap(m), origin='lower')
    pos = list(ax.get_position().bounds)
    fig.text(pos[0] - 0.01, pos[1], m, fontsize=10, horizontalalignment='right')
'''
        fig = pl.figure(figsize=(35,12))
        ax = fig.add_subplot(111)
#        t, ax = pl.subplots(1,1)


        p1 = ax.bar(ind,
                    test['wp_score'],
                    width,
                    color = 'c')

        p2 = ax.bar(ind,
                    test['wpr_score'],
                    width,
                    bottom = test['wp_score'],
                    color = 'violet')

        p3 = ax.bar(ind,
                    test['wbf_score'],
                    width,
                    bottom = test['wp_score'] + test['wpr_score'],
                    color = 'g')

        p4 = ax.bar(ind,
                    test['wpc_score'],
                    width,
                    bottom = test['wp_score'] + test['wpr_score'] + test['wbf_score'],
                    color = 'r')

        p5 = ax.bar(ind,
                    test['wbc_score'],
                    width,
                    bottom = test['wp_score'] + test['wpr_score'] + test['wbf_score'] + test['wpc_score'],
                    color = 'b')

        p6 = ax.bar(ind,
                    test['woa_score'],
                    width,
                    bottom = test['wp_score'] + test['wpr_score'] + test['wbf_score'] + test['wpc_score'] + test['wbc_score'],
                    color = 'm')


        ID = [test['propid'][i] +' '+ test['blockid'][i] for i in range(0, len(test))]

        ax.set_ylabel('Priority Score')
        ax.set_xlabel('Block ID')
        ax.set_xticks (ind + width/2.)
        ax.set_xticklabels(ID, rotation = 90 )
        ax.set_ylim(-1,10)

        fig.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]),
                   ('wP_score', 'wPR_score', 'wBF_score', 'wPC_score', 'wBC_score', 'wOA_score'))
#        fig.tight_layout()
        fig.subplots_adjust(left=None, bottom=0.20, right=None, top=None,
                            wspace=None, hspace=None)
        fig.show()

        pl.show()



#    pl.hist()
#    s0_ref = [p0]*len(PC)
#    s1_ref = [p1]*len(PC)
#    s2_ref = [p2]*len(PC)
#    s3_ref = [p3]*len(PC)
#    s4_ref = [p4]*len(PC)
#
#    s1 = p1 + PC_score(PC)
#    s2 = p2 + PC_score(PC)
#    s3 = p3 + PC_score(PC)
#
#    fig = pl.figure(figsize=(10,8))
#    pl.plot(PC, s0_ref, '-b', label='P0')
#    pl.plot(PC, s1_ref, '-g', label='P1')
#    pl.plot(PC, s2_ref, '-r', label='P2')
#    pl.plot(PC, s3_ref, '-c', label='P3')
#    pl.plot(PC, s4_ref, '-m', label='P4')
#
#    pl.plot(PC, s1, '--g', label='P1_override')
#    pl.plot(PC, s2, '--r', label='P2_override')
#    pl.plot(PC, s3, '--c', label='P3_override')
#
#    pl.title('Program completion')
#    pl.xlabel('Program Completion (%)')
#    pl.ylabel('Score')
#    pl.legend(loc=(1,0.0))
#
#    pl.ylim(-1.2,8)
#    pl.show()


