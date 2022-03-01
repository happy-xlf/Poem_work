#-*- coding:utf-8 -*-

from pyhanlp import *


#1.分词
sentence = "我爱北京天安门，天安门上放光彩"
#返回一个list，每个list是一个分词后的Term对象，可以获取word属性和nature属性，分别对应的是词和词性
# terms = HanLP.segment(sentence )
# for term in terms:
# 	print(term.word,term.nature)


# document = "水利部水资源司司长陈明忠9月29日在国务院新闻办举行的新闻发布会上透露，" \
#            "根据刚刚完成了水资源管理制度的考核，有部分省接近了红线的指标，" \
#            "有部分省超过红线的指标。对一些超过红线的地方，陈明忠表示，对一些取用水项目进行区域的限批，" \
#            "严格地进行水资源论证和取水许可的批准。"

#提取document的两个关键词
# print(HanLP.extractKeyword(document, 2))

#提取ducument中的3个关键句作为摘要
# print(HanLP.extractSummary(document,3))

#依存句法分析
#print(HanLP.parseDependency("徐先生还具体帮助他确定了把画雄鹰、松鼠和麻雀作为主攻目标。"))

#短语提取
text = "在计算机音视频和图形图像技术等二维信息算法处理方面目前比较先进的视频处理算法"
phraseList = HanLP.extractPhrase(text, 10)
print(phraseList)




# word='早年经历苏轼于宋仁宗景祐三年十二月十九日（1037年1月8日）出生于眉州眉山，是初唐大臣苏味道之后。苏轼的祖父是苏序，表字仲先，祖母史氏。苏轼的父亲苏洵，即《三字经》里提到的“二十七，始发奋”的“苏老泉”。苏洵发奋虽晚，但是很用功。苏轼其名“轼”原意为车前的扶手，取其默默无闻却扶危救困，不可或缺之意。苏轼生性放达，为人率真，深得道家风范。好交友，好美食，创造许多饮食精品，好品茗，亦雅好游山林。进京应试嘉祐元年（1056年），苏轼首次出川赴京，参加朝廷的科举考试。苏洵带着二十一岁的苏轼，十九岁的苏辙，自偏僻的西蜀地区，沿江东下，于嘉祐二年（1057年）进京应试。当时的主考官是文坛领袖欧阳修，小试官是诗坛宿将梅尧臣。这两人正锐意诗文革新，苏轼那清新洒脱的文风，一下子把他们震动了。策论的题目是《刑赏忠厚之至论》，苏轼的《刑赏忠厚之至论》获得主考官欧阳修的赏识，却因欧阳修误认为是自己的弟子曾巩所作，为了避嫌，使他只得第二。苏轼在文中写道：“皋陶为士，将杀人。皋陶曰杀之三，尧曰宥之三。”欧、梅二公既叹赏其文，却不知这几句话的出处。及苏轼谒谢，即以此问轼，苏轼答道：“何必知道出处！”欧阳修听后，不禁对苏轼的豪迈、敢于创新极为欣赏，而且预见了苏轼的将来：“此人可谓善读书，善用书，他日文章必独步天下。”名动京师在欧阳修的一再称赞下，苏轼一时声名大噪。他每有新作，立刻就会传遍京师。当父子名动京师、正要大展身手时，突然传来苏轼苏辙的母亲病故的噩耗。二兄弟随父回乡奔丧。嘉祐四年十月守丧期满回京，嘉祐六年（1061年），苏轼应中制科考试，即通常所谓的“三年京察”，入第三等，为“百年第一”，授大理评事、签书凤翔府判官。四年后还朝判登闻鼓院。治平二年，苏洵病逝，苏轼、苏辙兄弟扶柩还乡，守孝三年。三年之后，苏轼还朝，震动朝野的王安石变法开始了。苏轼的许多师友，包括当初赏识他的恩师欧阳修在内，因反对新法与新任宰相王安石政见不合，被迫离京。朝野旧雨凋零，苏轼眼中所见，已不是他二十岁时所见的“平和世界”。 自请出京熙宁四年（1071年）苏轼上书谈论新法的弊病。王安石很愤怒，让御史谢景在皇帝跟前说苏轼的过失。苏轼于是请求出京任职：熙宁四年至熙宁七年（1074年）被派往杭州任通判、熙宁七年秋调往密州（山东诸城）任知州、熙宁十年（1077年）四月至元丰二年（1079年）三月在徐州任知州、元丰二年四月调往湖州任知州。革新除弊，因法便民，颇有政绩。乌台诗案元丰二年（1079年），苏轼四十三岁，调任湖州知州。上任后，他即给皇上写了一封《湖州谢表》，这本是例行公事，但苏轼是诗人，笔端常带感情，即使官样文章，也忘不了加上点个人色彩，说自己“愚不适时，难以追陪新进”，“老不生事或能牧养小民”，这些话被新党抓了辫子，说他是“愚弄朝，妄自尊大”，说他“衔怨怀怒”，“指斥乘舆”，“包藏祸心”，讽刺政府，莽撞无礼，对皇帝不忠，如此大罪可谓死有余辜了。他们从苏轼的大量诗作中挑出他们认为隐含讥讽之意的句子，一时间，朝廷内一片倒苏之声。这年七月二十八日，苏轼上任才三个月，就被御史台的吏卒逮捕，解往京师，受牵连者达数十人。这就是北宋著名的“乌台诗案”（乌台，即御史台，因其上植柏树，终年栖息乌鸦，故称乌台）。乌台诗案这一巨大打击成为他一生的转折点。新党们非要置苏轼于死地不可。救援活动也在朝野同时展开，不但与苏轼政见相同的许多元老纷纷上书，连一些变法派的有识之士也劝谏神宗不要杀苏轼。王安石当时退休金陵，也上书说：“安有圣世而杀才士乎？”在大家努力下，这场诗案就因王安石“一言而决”，苏轼得到从轻发落，贬为黄州（今湖北黄冈）团练副使，本州安置，受当地官员监视。苏轼坐牢103天，几次濒临被砍头的境地。幸亏北宋时期在太祖赵匡胤年间既定下不杀士大夫的国策，苏轼才算躲过一劫。被贬黄州出狱以后，苏轼被降职为黄州（今湖北黄冈市）团练副使（相当于现代民间的自卫队副队长）。这个职位相当低微，并无实权，而此时苏轼经此一役已变得心灰意冷，苏轼到任后，心情郁闷，曾多次到黄州城外的赤壁山游览，写下了《赤壁赋》、《后赤壁赋》和《念奴娇·赤壁怀古》等千古名作，以此来寄托他谪居时的思想感情。于公余便带领家人开垦城东的一块坡地，种田帮补生计。“东坡居士”的别号便是他在这时起的。东山再起1084年（元丰七年），苏轼离开黄州，奉诏赴汝州就任。由于长途跋涉，旅途劳顿，苏轼的幼儿不幸夭折。汝州路途遥远，且路费已尽，再加上丧子之痛，苏轼便上书朝廷，请求暂时不去汝州，先到常州居住，后被批准。当他准备要南返常州时，神宗驾崩。常州一带水网交错，风景优美。他在常州居住，既无饥寒之忧，又可享美景之乐，而且远离了京城政治的纷争，能与家人、众多朋友朝夕相处。于是苏东坡终于选择了常州作为自己的终老之地。1085年，宋哲宗即位，高太后以哲宗年幼为名，临朝听政，司马光重新被启用为相，以王安石为首的新党被打压。苏轼复为朝奉郎知登州（蓬莱）。四个月后，以礼部郎中被召还朝。在朝半月，升起居舍人，三个月后，升中书舍人，不久又升翰林学士知制诰，知礼部贡举。当苏轼看到新兴势力拼命压制王安石集团的人物及尽废新法后，认为其与所谓“王党”不过一丘之貉，再次向皇帝提出谏议。他对旧党执政后，暴露出的腐败现象进行了抨击，由此，他又引起了保守势力的极力反对，于是又遭诬告陷害。苏轼至此是既不能容于新党，又不能见谅于旧党，因而再度自求外调。筑建苏堤元祐四年（1089年），苏轼任龙图阁学士知杭州。由于西湖长期没有疏浚，淤塞过半，“崶台平湖久芜漫，人经丰岁尚凋疏”，湖水逐渐干涸，湖中长满野草，严重影响了农业生产。苏轼来杭州的第二年率众疏浚西湖，动用民工20余万，开除葑田，恢复旧观，并在湖水最深处建立三塔（今三潭映月）作为标志。他把挖出的淤泥集中起来，筑成一条纵贯西湖的长堤，堤有6桥相接，以便行人，后人名之曰“苏公堤”，简称“苏堤”。苏堤在春天的清晨，烟柳笼纱，波光树影，鸟鸣莺啼，是著名的西湖十景之一“苏堤春晓”。“东坡处处筑苏堤”，苏轼一生筑过三条长堤。苏轼被贬颍州（今安徽阜阳）时，对颍州西湖也进行了疏浚，并筑堤。绍圣元年（1094年），苏轼被贬为远宁军节度副使，惠州（今广东惠阳）安置。年近6旬的苏轼，日夜奔驰，千里迢迢赴贬所，受到了岭南百姓热情的欢迎。苏轼把皇帝赏赐的黄金拿出来，捐助疏浚西湖，并修了一条长堤。为此，“父老喜云集，箪壶无空携，三日饮不散，杀尽村西鸡”，人们欢庆不已。如今，这条苏堤在惠州西湖入口处，像一条绿带，横穿湖心，把湖一分为二，右边是平湖，左边是丰湖。 流落儋州苏轼在杭州过得很惬意，自比唐代的白居易。但元祐六年（1091年），他又被召回朝。但不久又因为政见不合，元祐六年八月调往颍州任知州、元祐七年（1092年）二月任扬州知州、元祐八年（1093年）九月任定州知州。元祐八年高太后去世，哲宗执政，新党再度执政，绍圣元年（1094年）六月，别为宁远军节度副使，再次被贬至惠阳（今广东惠州市）。绍圣四年（1097年），年已62岁的苏轼被一叶孤舟送到了徼边荒凉之地海南岛儋州（今海南儋县）。据说在宋朝，放逐海南是仅比满门抄斩罪轻一等的处罚。他把儋州当成了自己的第二故乡，“我本儋耳氏，寄生西蜀州”。他在这里办学堂，介学风，以致许多人不远千里，追至儋州，从苏轼学。在宋代100多年里，海南从没有人进士及第。但苏轼北归不久，这里的姜唐佐就举乡贡。为此苏轼题诗：“沧海何曾断地脉，珠崖从此破天荒。”人们一直把苏轼看作是儋州文化的开拓者、播种人，对他怀有深深的崇敬。在儋州流传至今的东坡村、东坡井、东坡田、东坡路、东坡桥、东坡帽等等，表达了人们的缅怀之情，连语言都有一种“东坡话”。最后结局徽宗即位后，苏轼被调廉州安置、舒州团练副使、永州安置。元符三年四月（1100年）大赦，复任朝奉郎，北归途中，于建中靖国元年七月二十八日（1101年8月24日）卒于常州（今属江苏）。葬于汝州郏城县（今河南郏县），享年六十五岁。苏轼留下遗嘱葬汝州郏城县钧台乡上瑞里。次年，其子苏过遵嘱将父亲灵柩运至郏城县安葬。宋高宗即位后，追赠苏轼为太师，谥为“文忠”。'
#
# list=word.split("。")
# for it in list:
#     print(it)
#     conten_list = HanLP.segment(it)
#     arr = str(conten_list).split(" ")
#     print(arr)
#     ci=['nr','ns','t','ni']
#     for item in conten_list:
#         print(item.nature=='t')
#         if item.nature in ci:
#          print(item.word, item.nature)

# text = '杨超越在1998年7月31日出生于江苏省盐城市大丰区。'
# NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
# NER = NLPTokenizer.segment(text)
# print(NER)


# 中文人名识别

sentences = [
    "武大靖创世界纪录夺冠，中国代表团平昌首金",
    "区长庄木弟新年致辞",
    "凯瑟琳和露西（庐瑞媛），跟她们的哥哥们有一些不同。",
    "王国强、高峰、汪洋、张朝阳光着头、韩寒、小四",
    "张浩和胡健康复员回家了",
    "王总和小丽结婚了",
    "编剧邵钧林和稽道青说",
    "这里有关天培的有关事迹",]
CRFnewSegment = HanLP.newSegment("crf")
print(CRFnewSegment.seg(sentences[2]))

# 演示数词与数量词识别
sentences = [
    "十九元套餐包括什么",
    "九千九百九十九朵玫瑰",
    "壹佰块都不给我",
    "９０１２３４５６７８只蚂蚁",
    "牛奶三〇〇克*2",
    "ChinaJoy“扫黄”细则露胸超2厘米罚款",
]

StandardTokenizer = JClass("com.hankcs.hanlp.tokenizer.StandardTokenizer")

StandardTokenizer.SEGMENT.enableNumberQuantifierRecognize(True)
for sentence in sentences:
    print(StandardTokenizer.segment(sentence))

print("\n========== 演示数词与数量词 默认未开启 ==========\n")
CRFnewSegment.enableNumberQuantifierRecognize(True)
print(CRFnewSegment.seg(sentences[0]))














