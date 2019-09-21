import numpy
import random

def txtTolist(txt):
    lst = txt.split()

    new_list = []

    while len(lst) > 0:
        a = lst.pop(0)

        b = lst.pop(0)

        # print lst

        new_list.append((float(a), float(b)))

    return new_list


node_list = txtTolist("""
29.719204 -95.407239
29.718161 -95.406773
29.716810 -95.405990
29.717518 -95.408458
29.716111 -95.407739
29.714834 -95.408511
29.718543 -95.408987
29.714126 -95.408871
29.713436 -95.406521
29.713827 -95.406382
29.714646 -95.406021
29.714888 -95.406003
29.716444 -95.406740
29.717465 -95.412664
29.715116 -95.412680
29.711507 -95.400962
29.716366 -95.402021
29.718014 -95.402897
29.718921 -95.403363
29.719732 -95.403760
29.720364 -95.404061
29.714298 -95.400939
29.714484 -95.398954
29.720005 -95.403095
29.721291 -95.401765
29.720667 -95.401432
29.720835 -95.401003
29.722251 -95.399308
29.721645 -95.399008
29.721561 -95.399190
29.720592 -95.398696
29.720555 -95.398342
29.719949 -95.397988
29.719828 -95.398042
29.719045 -95.400284
29.717200 -95.400016
29.717768 -95.398407
29.719548 -95.397763
29.719250 -95.397634
29.719017 -95.397484
29.718709 -95.397312
29.717190 -95.398084
29.716018 -95.397470
29.719093 -95.396515
29.719363 -95.396633
29.719875 -95.396912
29.719573 -95.396772
29.720947 -95.396575
29.718565 -95.395485
29.720568 -95.393997
""")
text_data = """ 20180101
20180102
20180103
20180104
20180105
20180106
20180107
20180108
20180109
20180110
20180111
20180112
20180113
20180114
20180115
20180116
20180117
20180118
20180119
20180120
20180121
20180122
20180123
20180124
20180125
20180126
20180127
20180128
20180129
20180130
20180131
20180201
20180202
20180203
20180204
20180205
20180206
20180207
20180208
20180209
20180210
20180211
20180212
20180213
20180214
20180215
20180216
20180217
20180218
20180219
20180220
20180221
20180222
20180223
20180224
20180225
20180226
20180227
20180228
20180301
20180302
20180303
20180304
20180305
20180306
20180307
20180308
20180309
20180310
20180311
20180312
20180313
20180314
20180315
20180316
20180317
20180318
20180319
20180320
20180321
20180322
20180323
20180324
20180325
20180326
20180327
20180328
20180329
20180330
20180331
20180401
20180402
20180403
20180404
20180405
20180406
20180407
20180408
20180409
20180410
20180411
20180412
20180413
20180414
20180415
20180416
20180417
20180418
20180419
20180420
20180421
20180422
20180423
20180424
20180425
20180426
20180427
20180428
20180429
20180430
20180501
20180502
20180503
20180504
20180505
20180506
20180507
20180508
20180509
20180510
20180511
20180512
20180513
20180514
20180515
20180516
20180517
20180518
20180519
20180520
20180521
20180522
20180523
20180524
20180525
20180526
20180527
20180528
20180529
20180530
20180531
20180601
20180602
20180603
20180604
20180605
20180606
20180607
20180608
20180609
20180610
20180611
20180612
20180613
20180614
20180615
20180616
20180617
20180618
20180619
20180620
20180621
20180622
20180623
20180624
20180625
20180626
20180627
20180628
20180629
20180630
20180701
20180702
20180703
20180704
20180705
20180706
20180707
20180708
20180709
20180710
20180711
20180712
20180713
20180714
20180715
20180716
20180717
20180718
20180719
20180720
20180721
20180722
20180723
20180724
20180725
20180726
20180727
20180728
20180729
20180730
20180731
20180801
20180802
20180803
20180804
20180805
20180806
20180807
20180808
20180809
20180810
20180811
20180812
20180813
20180814
20180815
20180816
20180817
20180818
20180819
20180820
20180821
20180822
20180823
20180824
20180825
20180826
20180827
20180828
20180829
20180830
20180831
20180901
20180902
20180903
20180904
20180905
20180906
20180907
20180908
20180909
20180910
20180911
20180912
20180913
20180914
20180915
20180916
20180917
20180918
20180919
20180920
20180921
20180922
20180923
20180924
20180925
20180926
20180927
20180928
20180929
20180930
20181001
20181002
20181003
20181004
20181005
20181006
20181007
20181008
20181009
20181010
20181011
20181012
20181013
20181014
20181015
20181016
20181017
20181018
20181019
20181020
20181021
20181022
20181023
20181024
20181025
20181026
20181027
20181028
20181029
20181030
20181031
20181101
20181102
20181103
20181104
20181105
20181106
20181107
20181108
20181109
20181110
20181111
20181112
20181113
20181114
20181115
20181116
20181117
20181118
20181119
20181120
20181121
20181122
20181123
20181124
20181125
20181126
20181127
20181128
20181129
20181130
20181201
20181202
20181203
20181204
20181205
20181206
20181207
20181208
20181209
20181210
20181211
20181212
20181213
20181214
20181215
20181216
20181217
20181218
20181219
20181220
20181221
20181222
20181223
20181224
20181225
20181226
20181227
20181228
20181229
20181230
20181231
20190101
20190102
20190103
20190104
20190105
20190106
20190107
20190108
20190109
20190110
20190111
20190112
20190113
20190114
20190115
20190116
20190117
20190118
20190119
20190120
20190121
20190122
20190123
20190124
20190125
20190126
20190127
20190128
20190129
20190130
20190131
20190201
20190202
20190203
20190204
20190205
20190206
20190207
20190208
20190209
20190210
20190211
20190212
20190213
20190214
20190215
20190216
20190217
20190218
20190219
20190220
20190221
20190222
20190223
20190224
20190225
20190226
20190227
20190228
20190301
20190302
20190303
20190304
20190305
20190306
20190307
20190308
20190309
20190310
20190311
20190312
20190313
20190314
20190315
20190316
20190317
20190318
20190319
20190320
20190321
20190322
20190323
20190324
20190325
20190326
20190327
20190328
20190329
20190330
20190331
20190401
20190402
20190403
20190404
20190405
20190406
20190407
20190408
20190409
20190410
20190411
20190412
20190413
20190414
20190415
20190416
20190417
20190418
20190419
20190420
20190421
20190422
20190423
20190424
20190425
20190426
20190427
20190428
20190429
20190430
20190501
20190502
20190503
20190504
20190505
20190506
20190507
20190508
20190509
20190510
20190511
20190512
20190513
20190514
20190515
20190516
20190517
20190518
20190519
20190520
20190521
20190522
20190523
20190524
20190525
20190526
20190527
20190528
20190529
20190530
20190531
20190601
20190602
20190603
20190604
20190605
20190606
20190607
20190608
20190609
20190610
20190611
20190612
20190613
20190614
20190615
20190616
20190617
20190618
20190619
20190620
20190621
20190622
20190623
20190624
20190625
20190626
20190627
20190628
20190629
20190630
20190701
20190702
20190703
20190704
20190705
20190706
20190707
20190708
20190709
20190710
20190711
20190712
20190713
20190714
20190715
20190716
20190717
20190718
20190719
20190720
20190721
20190722
20190723
20190724
20190725
20190726
20190727
20190728
20190729
20190730
20190731
20190801
20190802
20190803
20190804
20190805
20190806
20190807
20190808
20190809
20190810
20190811
20190812
20190813
20190814
20190815
20190816
20190817
20190818
20190819
20190820
20190821
20190822
20190823
20190824
20190825
20190826
20190827
20190828
20190829
20190830
20190831
20190901
20190902
20190903
20190904
20190905
20190906
20190907
20190908
20190909
20190910
20190911
20190912
20190913
20190914
20190915
20190916
20190917
20190918
20190919
20190920
"""

dict1 = {}

def format(int):

    if int < 10 :

        return str(0)+str(int)

    else:
        return str(int)


def generate_Dates():

    days_per_mo = [None,31,28,31,30,31,30,31,31,30,31,30,31]

    last_string = []

    for year in [2018,2019]:

        for month in range(1,13):

            breakflag = False

            for days in range(1, days_per_mo[month] + 1):

                if year == 2019 and month == 9 and days == 21:
                    breakflag = True

                    break

                last_string.append(str(year)+format(month)+format(days))

            if breakflag:
               break

    return last_string

dates = generate_Dates()



def give_depths(precipitation):

    nodes_to_depths_for_each_day = {}

    for item in node_list:

        coeff = numpy.random.normal(0.7,0.05)

        integral = 0
        list_for_node = []

        for i in range(len(dates)):

            integral += 20*(precipitation[i] - coeff)

            if integral >= 0:

                list_for_node.append(integral)

            else:
                integral = 0
                list_for_node.append(integral)

        nodes_to_depths_for_each_day[item] = list_for_node

    return nodes_to_depths_for_each_day

precipitation = [numpy.random.normal(0.5,0.125) for i in range(len(dates))]

print (precipitation)
print (give_depths(precipitation))