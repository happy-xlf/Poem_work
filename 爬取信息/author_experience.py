# coding:utf-8
#代码内容
#抽取诗人的个人经历：时间，地点，人物，事件，围绕这四个方面来抽取
import re
from pyhanlp import *
import pandas as pd
#人名“nr“
#地名“ns”
#机构名“nt”

import os
#获取文件夹下的所有文件名
def get_filename(path,filetype):  # 输入路径、文件类型例如'.xlsx'
    name = []
    for root,dirs,files in os.walk(path):
        for i in files:
            if os.path.splitext(i)[1]==filetype:
                name.append(i)
    return name            # 输出由有后缀的文件名组成的列表

#添加自定义语料库：作者名，朝代年号
def add_user_dict():
    CustomDictionary = JClass("com.hankcs.hanlp.dictionary.CustomDictionary")
    #添加作者名字
    author_data=pd.read_excel('./data2/author_new.xlsx')
    name=author_data.author
    for it in name:
        CustomDictionary.add(it,"nr")
    #添加时间词
    time=[]
    file = 'data3/'
    lists = get_filename(file, '.xlsx')
    for it in lists:
        newfile = file + it
        dd=pd.read_excel(newfile).year_hao
        time.extend(dd)
    #print(time)
    for t in time:
        #print(t)
        CustomDictionary.add(t,"t")

#处理作者关键信息：时间，人物，地点，事件
def key_print(lists,text,new_author):
    time = []
    where = []
    author = []
    move=[]
    for it in lists:
        simple = it.split('/')
        if simple[1] == 't':
            time.append(simple[0])
        elif simple[1] == 'nr':
            author.append(simple[0])
        elif simple[1] == 'ns':
            where.append(simple[0])
        elif simple[1] == 'v':
            move.append(simple[0])

    if len(time)!=0 and ( len(move)!=0 or len(where)!=0 ):
        newtime=""
        for it in time:
            if bool(re.search(r'\d',it)) and it.find('年')!=-1:
                newtime=it
        f1=False
        if newtime!="":
            f1=True
            #print("时间：" + newtime)
            #保存时间
            data_list.append(newtime)
        else:
            if len(data_list)!=0:
                f1=True
                #print("时间："+str(data_list[len(data_list)-1]))
                data_list.append(data_list[len(data_list)-1])
        if f1:
            #时间必须有，才能采集后面的
            if len(author)!=0:
                author=list(set(author))
                author_list.append(",".join(author))
                #print("人物:"+" ".join(author))
            else:
                author_list.append(new_author)
                #print("人物:"+new_author)
            if len(where)!=0:
                where_list.append(",".join(where))
                #print("地点：" + " ".join(where))
            else:
                where_list.append("无")
                #print("地点：无")
            #处理事件
            things=[]
            if len(move)!=0:
                thing_list=re.split('[，。；]+',text)
                for v in move:
                    for it in thing_list:
                        if it.find(v)!=-1:
                                things.append(it)
                #去重
                set_things=list(set(things))
                things_list.append(",".join(set_things))
                #print("事件：")
                #print(set_things)
            else:
                things_list.append("无")
                #print("事件：无")
    #事件：动作+人物+地点


#用crf模型提取词性
def demo_CRF_lexical_analyzer(text,new_author):
    global bg_time
    CRFnewSegment = HanLP.newSegment("crf")
    term_list = CRFnewSegment.enableCustomDictionaryForcing(True).seg(text)
    ans=[]
    #'p'介词
    #'ns'地名
    #'t'时间词
    #'nz'其他专名
    #'j'简称略语
    #'m'数词
    #'n'名词
    # 人名“nr“
    # 地名“ns”
    # 机构名“nt”
    #至少得有时间词与人物
    f1=False
    f2=False
    lists=['n','nr','v','nz','ns','t']
    tmp=[]
    for it in term_list:
        if str(it.nature) in lists:
            tmp.append(str(it.word)+"/"+str(it.nature))
            if str(it.nature)=='t':
                if bool(re.search(r'\d',it.word)):
                    #这一步保存bg_time是为后面没有具体时间的事件，提供时间
                    bg_time=str(it.word)
                    f1 = True
            elif str(it.nature)=='ns':
                f2=True
    if f1:
        #print(tmp)
        key_print(tmp,text,new_author)
    else:
        if f2:
            tmp.append(bg_time+"/t")
            #print(tmp)
            key_print(tmp,text,new_author)
import xlwt

#进行诗人个人生平分析
def author_identity(text,author):
    lists = text.split("。")

    for it in lists:
        #print(it)
        demo_CRF_lexical_analyzer(it,author)
    #print("============分析结果================")
    #print(len(data_list))
    #for i in range(len(data_list)):
        #print(data_list[i], author_list[i], where_list[i], things_list[i])

    #print("===========保存数据================")
    if len(data_list)!=0:
        xl = xlwt.Workbook()
        # 调用对象的add_sheet方法
        sheet1 = xl.add_sheet('sheet1', cell_overwrite_ok=True)

        sheet1.write(0, 0, "data")
        sheet1.write(0, 1, "author")
        sheet1.write(0, 2, "wheres")
        sheet1.write(0, 3, "things")
        for i in range(0, len(data_list)):
            sheet1.write(i + 1, 0, data_list[i])
            sheet1.write(i + 1, 1, author_list[i])
            sheet1.write(i + 1, 2, where_list[i])
            sheet1.write(i + 1, 3, things_list[i])

        xl.save("./author2/"+author+".xlsx")

#清洗作者，只要包含个人生平的作者信息
def read_author():
    author_list = pd.read_excel('./data2/author_new.xlsx').fillna('无')
    author_name = author_list.author
    author_experience = author_list.experience
    for i in range(len(author_experience)):
        if author_experience[i]!='无':
            new_author_name.append(author_name[i])
            new_author_experience.append(author_experience[i])

#测试
def read_one():
    text='初显将才韩世忠出身于普通农民家庭。自幼喜欢练武，学习刻苦认真。少年时期就有过人的力气。性情憨直善良，喜欢行侠仗义。不慕功名。韩世忠长到十六、七岁时，生得身材魁梧高大，浑身是劲儿，勇力过人，家乡有人对他说，有如此好的功夫，应该去当兵为国效力。于是，年仅十七岁他就参军当了一名士卒。韩世忠所在的部队驻在西北地区，经常与西夏军队发生冲突。韩世忠入伍不久就参加了战斗，因作战勇敢就由士卒升为小队长，只管十几个人。官职虽小，但韩世忠仍能积极负责，他领导的那些士兵都比他年纪大，可是韩世忠作战勇敢，处事公道正派，说话正直在理，所以大家都听他的。有一次宋军攻打西夏的一座城池，久攻不下，韩世忠打红了眼，一个人爬墙冲进去，杀死守城的敌军头领，把他的脑袋扔出城外，宋军受到鼓舞，一涌而上，攻下城池。不久，西夏王的监军驸马亲率夏军向宋军反击，宋军有畏怯之状。韩世忠问清驸马的身份和作用，然后率几名敢死士卒，冲入敌阵，这突如其来的冲击让敌人惊慌失措，韩世忠冲入敌阵直奔元帅帐，还没等西夏兵明白过来，手起刀落，将西夏监军驸马的头砍了下来。西夏兵大乱，争相奔逃。宋军将领都称赞韩世忠的勇敢，说他年纪虽小，却是个不可多得的将才。因此，经略使上报朝廷，请求破格提拔韩世忠。可是，当时主持边事的童贯却怀疑汇报的真实性，只同意给韩世忠升一级。抗击金兵1121年（宣和三年），宋政权派出的部队与金兵战于燕山南。几路兵马均被金兵打败。韩世忠率五十余骑巡逻于滹沱河上，不巧与金兵大队人马遭遇。金兵是一支两千人的骑兵主力。韩世忠遇事冷静而果断，他告诉士卒：“慌乱就等于死，不要乱动，一切听我安排。”他让一个叫苏格的小队长率部分人抢占高坡，列阵其上，观而不动。又派出十余个骑士，把在河准备抢渡的散乱宋军组织起来，得众数百，让他们列阵击鼓呐喊。然后，他率几名敢死骑士，径直冲入金兵队阵之中，专砍打旗的金兵，连杀几个之后，其余举旗的纷纷将旗放倒，河边的宋军士卒击鼓高喊：“金兵败啦！金兵败啦！”倾刻间金兵大乱，苏格率占据高地的骑兵自上而下杀来，金兵丢下上百具尸体，乱纷纷向北逃去，韩世忠又追了一程才收住坐骑。1126年（靖康元年）十月，正在滹沱河一带担任防守任务的韩世忠被金兵数万追逼退入赵州城内。敌兵围城数重。城中兵少粮乏，军心不稳，有人主张弃城而遁。韩世忠传令下去，有敢言弃城者斩。当天夜里，天降大雪，韩世忠选精壮士卒三百人，悄悄出城，偷偷摸进金兵围城主帅营帐，杀死主帅，后偷袭金兵驻地，挑起金兵内部误相攻杀。一夜大战，金兵死伤过半，当得知主将被杀，看到遍地都是自家兄弟的尸体，流出的血把雪都染成了红色的，金兵无心再战，溃散退去。韩世忠在河北一带坚持抗金斗争数年，官阶不高，所率兵马并不多，但是战无不胜，攻无不克，因此，其威名震慑金兵。解救高宗靖康之变，开封城陷，宋徽宗和宋钦宗父子两人作了金兵的俘虏。徽宗的第九个儿子康王赵构在南京（商丘）当了皇帝，是为宋高宗。这是南宋小朝廷的第一任皇帝。赵构不想有所作为，只图苟且偷安。在商丘就任之后，一路被金兵追击，从商丘跑到杨州，又从杨州跑到杭州，最后跑到海上去躲避金兵。在岳飞等将的抵抗下，金兵退出江南，赵构又从海上返回杭州。为了平息舆论，他罢免了投降派宰相汪伯彦、黄潜善等人，任朱胜非为宰相，王渊掌枢密院事，吕颐浩为江东安抚制背使。将官苗傅、刘正彦对朝廷不满发动兵变，杀死了王渊和宦官康履，逼高宗让位给三岁的儿子。吕颐浩约韩世忠、张浚等大将平息叛乱，解救高宗。韩世忠身边兵不多，就在盐城一带收集散卒，组织起几十人的部队，从海上来到常熟。约见张浚等人进兵到秀州，然后诈称休兵，不再前进。实际暗中作攻城的准备。苗傅、刘正彦知韩世忠来攻，就俘虏韩世忠的妻子梁红玉作为人质。宰相朱胜非已假意屈从苗、刘，对他们说，与其逼韩世忠战，不若遣梁红玉去抚慰韩世忠，只要韩世忠能降，大事可成矣！苗、刘果然让使者跟随梁红玉去见韩世忠。梁氏回到丈夫身边，使者到来后，韩世忠烧了诏书，砍了使者，下令进攻杭州。韩世忠在杭州北关击败叛军防守部队，苗、刘惊惧，率二千主力逃跑。韩世忠救出高宗赵构，高宗告诉他，宫中的中军统制吴湛和苗、刘是一伙的，此贼不除，宫中不安。恰在此时，吴湛率兵前宋迎接韩世忠，伸手与韩世忠相握，韩世忠力大，顺势捏断了吴湛的手指，喝令拿下，与其他叛将一并斩于市曹。苗、刘之乱遂平，南宋小朝廷稳定下来。韩世忠功劳最大，从此成了高宗的亲信，被任命为武胜军节度使、御营左军都统制。此次平乱，确立了韩世忠在南宋将领中的名声和地位。围困兀术1129年（建炎三年），金兵再次南下，突破长江天险，攻破了建康（今南京）等重要城镇，躲在杭州的宋高宗赵构又要逃跑。韩世忠面见高宗，慷慨陈词：“国家已丢失河北、河东、山东诸地，再把江淮丢掉，还有何处可去?”赵构根本听不进去，他所想的只有保住性命。赵构任命韩世忠为浙西制置使，防守镇江，而赵构则跟随投降势力逃到了海上。镇江其时已处敌后，韩世忠领命仅率所部八千人急赶镇江．金兵在江南抢掠一阵之后陆续退去。韩世忠驻守于松江、江湾、海口一带，听到金兵撤退的消息，韩世忠立即分兵把守要地，准备乘机斩杀金兵。埋伏的宋兵差一点儿活捉金兵元帅兀术。兀术乃好战之将，他给韩世忠下了战书，约期会战。韩世忠与敌约定日期，在江中会战。金兵因不习水战，韩世忠就利用敌人这一弱点，封锁长江，几次交战大败金兵，还活捉了兀术的女婿龙虎大王。兀术不敢再战，率十万兵马退入黄天荡，企图从这里过江北逃。黄天荡是江中的一条断港，早已废置不用，只有进去的路，没有出去的路。韩世忠见金兵误入岐途，就抓住这一难得的机会，待金兵进去之后，立即率兵封锁住出口。兀术率金兵被困于黄天荡内，进退无门，眼见十万士卒就要被饿死荡中，兀术派使者与韩世忠讲和，愿意把抢掠的财物全部送还，向韩世忠献宝马，以此为条件，换条退路，韩世忠一概不答应。兀术只好重金悬赏求计。兀术重金从一个汉奸那里买来了良策。黄天荡内有一条老鹳河，直通建康秦淮河，因年久不用而淤塞，派人挖通即可从水路逃出。兀术派人，一夜之间挖通此河，企图从水道入建康。途经牛头山，刚收复建康的岳飞在此处驻有军队，见敌人从这里出来，立即调集大军猛击，兀术只好退回黄天荡。韩世忠准备置敌于死地，他派人打制铁索和铁钩，一遇敌船定要消灭。眼看敌人无计可施，只有等死，此时又一个汉奸向金兵献策，教他们乘宋军扬帆行船之时，集中火箭射船帆，烧毁宋军战船，这样便可逃出黄天荡。兀术大喜，依计而行，果然有效，宋军船只被烧毁许多，金兵乘机冲出黄天荡，向北逃过长江，撤回黄河以北地区。韩世忠仅用八千军队，困敌十万兵马于黄天荡，战四十八天，歼敌万余。此战意义非凡，激起了江淮人民的抗金情绪，使人民看到了金兵并不可怕。韩世忠因黄天荡战役以巧制敌，其威武雄姿和将帅风范传遍江淮地区。大仪镇大捷1134年（绍兴四年），韩世忠任建康、镇江、淮东宣抚使驻扎镇江。岳飞收复襄阳（今湖北襄樊）等六郡后，伪齐主刘豫派人向金乞援，金太宗完颜晟命元帅左监军完颜宗弼率军5万，与伪齐军联合，自淮阳(今江苏邳县西南)等地，兵分两路，南下攻宋。企图先以骑兵下滁州（今属安徽），步兵克承州（今江苏高邮），尔后渡江会攻临安（今浙江杭州）。九月二十六日，金军攻楚州（今江苏淮安）。宋淮东宣抚使韩世忠军自承州退守镇江（今属江苏）。宋廷急遣工部侍郎魏良臣等赴金军乞和，并命韩世忠自镇江北上扬州，以阻金军渡江。十月初四，韩世忠率兵进驻扬州后，即命部将解元守承州，邀击金军步兵；自率骑兵至大仪镇（今江苏扬州西北）抵御金骑兵。十二日，魏良臣路一行过扬州，韩世忠故意出示避敌守江的指令，佯作回师镇江姿态。待魏良臣走后，韩世忠立即率精骑驰往大仪镇，在一片沼泽地域将兵马分为5阵，设伏20余处，准备迎击金军。翌日，金将万夫长聂儿孛堇从魏良臣口中得知韩世忠退守镇江，遂命部将挞孛也等数百骑直趋扬州附近江口，进至大仪镇东。韩世忠亲率轻骑挑战诱敌，将金军诱入伏击区，宋伏兵四起，金军猝不及防，弓刀无所施。韩世忠命精骑包抄合击，并命背嵬军各持长斧，上劈人胸，下砍马足，金军陷于泥淖之中，伤亡惨重，金将挞孛也等200余人被俘，其余大部被歼。捷报传到杭州，群臣入贺，高宗命令令对韩世忠及各部将论功行赏。大仪镇之捷，是南宋十三处战功之一，当时论者有认为这是南宋中兴武功第一。斥责秦桧在南宋政权内部始终存在着抗战与投降之间的斗争。以岳飞、韩世忠等战将为代表的主战派，拒绝妥协投降，反对与金议和；而以秦桧等文臣为首的士族势力，企图偏安一隅，因此，反对抗战，主张妥协议和，最终走向了屈膝投降的道路。韩世忠不管率兵多少，从不畏惧金兵，不管在什么地方，闻警则动，见敌则战。他坚决主张打过长江、打过黄河去，收复所有失地。1140年，在金兵大肆南侵的形势下，韩世忠竟然率领为数不多的军队包围了被金兵占领的淮阳，然后大败金兵主力于泇口镇。在这个时期，抗战派略占上风。韩世忠因功被封为太保，封英国公，兼河南、河北诸路讨使。正当韩世忠招兵买马，扩大队伍准备大干之时，形势急转直下，投降派势力获得了宋高宗的支持，因为岳飞率领的抗金大军已在中原一带大得其势。宋高宗所担心的是一旦打败金兵，迎回他的父皇（徽宗）和哥哥（钦宗）。所以，在他的支持下，秦桧收了韩世忠、岳飞、张俊三位抗金大将的兵权。秦桧一日之内连发十二道金牌，强令处在抗金最前线的岳飞罢兵回临安。因韩世忠对宋高宗有救驾之恩，因此，升枢密使，明为升官，实为剥夺其兵权。岳飞父子被捕下狱，秦桧独霸朝政，无人敢言，但韩世忠不管这一套，他面见秦桧，当面指斥道：“岳飞父子何罪？为何将其关押？”秦桧答曰：“飞子云与张宪书，虽不明，其事体莫须有”。韩世忠斥道：“‘莫须有’三字能服天下吗？”好友劝他，得罪秦桧日后难逃报复，而韩世忠却说：“今吾为已而附合奸贼，死后岂不遭太祖铁杖？”韩世忠见岳飞父子被处死，大好的抗金形势白白丧失，自己又无能为力，便毅然辞去枢密使的官职，终日借酒消愁。晚年喜释、老，自号清凉居士。最终还是忧愤而死，卒于1151年（绍兴二十一年）。'
    author='韩世忠'
    author_identity(text, author)

#开始处理
if __name__ == '__main__':
    add_user_dict()
    #提取最终的包含个人经历的作者
    new_author_name = []
    new_author_experience = []
    read_author()
    #输出一共多少个
    print("一共："+str(len(new_author_name)))
    for i in range(len(new_author_name)):
        #存储上一个时间
        bg_time = ""
        print("第"+str(i)+"个")
        author=new_author_name[i]
        text=new_author_experience[i]
        # 时间序列
        data_list = []
        author_list = []
        where_list = []
        things_list = []
        author_identity(text,author)