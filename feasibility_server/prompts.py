# -*- coding: utf-8 -*-

# first_feasibility_report_prompt = """你现在是一个从事文字编写的专业人员，现在需要攥写研究报告的目的和意义，
#             参考材料如下： {}，参考材料到此结束。
#             输出格式需要为以下格式，例如：
#             1. 项目研究的必要性
#             2. 项目的总体目标
#             示例到此为止。
#             注意：生成的内容必须按照以上示例的格式进行生成，但是不能引用以上示例的内容！生成的内容必须根据参考材料进行二次创作！
# """

# second_feasibility_report_prompt = """你现在是一个从事文字编写的专业人员，现在需要攥写项目研究的背景，
#             参考材料如下：{}，参考材料到此结束。
#             输出格式需要为以下格式，例如：
#             项目研究的背景
#             注意：生成的内容必须按照以上示例的格式进行生成，但是不能引用以上示例的内容！生成的内容必须根据参考材料进行二次创作，只能是介绍背景！
# """

# third_feasibility_report_prompt = """你现在是一个从事文字编写的专业人员，现在需要攥写项目研究目标及主要研究内容，
#             参考材料如下：{}，参考材料到此结束。
#             输出格式需要为以下格式，例如：
#             研究目标及主要研究内容
#             1. 课题（任务）
#             研究目标：
#             主要研究内容：
#             2. 课题（任务）
#             研究目标：
#             主要研究内容：
#             3. 课题（任务）
#             研究目标：
#             主要研究内容：
#             4. 课题（任务）
#             研究目标：
#             主要研究内容：
#             5. 课题（任务）
#             研究目标：
#             主要研究内容：
#             示例到此为止。
#             注意：生成的内容必须严格按照以上示例的格式进行生成，但是不能引用以上示例的内容！生成的内容必须根据参考材料进行二次创作！
# """

feasibility_report_prompt = """你现在是一个从事技术文档编写的技术人员，现在需要从学术的角度详细撰写一段关于\"{}\"的文字,
            主题如下：\n\"{}\"，主题到此结束。 
            参考材料如下：\n\"{}\"，参考材料到此结束。
            输出格式需要为以下格式，例如： 
            \n\"{}\"
            注意：生成内容不要包含序号，生成内容的序号必须严格按照以上示例的格式进行生成，生成的内容不能直接引用以上材料的内容！生成的内容必须根据参考材料进行二次创作！
"""

dir_feasibility_report_prompt = """你现在是一个从事技术文档编写的技术人员， 你需要根据下面的材料攥写大纲， 
            主题如下：\n\"{}\"，主题到此结束。 
            参考材料如下：\n\"{}\"，参考材料到此结束。 
            输出大纲序号需要为以下格式，例如：
            一、
                1.1
                1.2
            二、
                2.1
                2.2
            三、
                3.1
                3.2
            四、
                4.1
                4.2
            五、
                5.1
                5.2
            注意：生成内容的序号必须严格按照以上示例的格式规律进行生成，生成的内容不能直接引用以上材料的内容！生成的内容必须根据参考材料进行二次创作！
"""

all_feasibility_report_prompt = """
            写作任务如下：\n\"{}\"，写作任务到此结束。 \n
            参考材料如下：\n\"{}\"，参考材料到此结束。\n
            注意：生成内容不能直接引用参考材料！生成内容必须进行二次创作！
"""

# pca_feasibility_report_prompt = """作为一名专业的写作大师，你的任务是总结和浓缩用户输入内容的要点，提供完善的摘要概述。输入内容可以变化，并且可以包括各种主题，例如文章、文章或文档。你的总结应该捕捉输入的基本元素，以清晰有序的方式突出其主要想法、论点或见解。您的回复应该提供一个结构良好、重点突出的markdown格式的摘要，有效地提取输入内容的核心方面。它应该保持原意和意图，同时以更简洁、更易于理解的格式呈现。此外，你的摘要应该足够灵活，以容纳广泛的输入内容，并允许创造性和原创的材料浓缩。现在请帮我根据用户提供的文本，生成一篇内容完善的摘要。用户提供文本如下：
# 间变性大T细胞淋巴瘤和乳房假体：文献综述
# 【摘要】 背景与目的单例病例报告和单例病例对照研究均已显示，乳房假体与间变性淋巴瘤激
# 酶阴性的间变性大T细胞淋巴瘤(anaplastic large T—cell lymphoma，ALCL)之间有相关关系，但没有因果
# 关系证据。ALCL是一种罕见的非霍奇金淋巴瘤。本文综述了已发表的证据，包括病例报告和流行病学
# 研究。方法在PubMed数据库中，检索已报道的与乳房相关ALCL病例的文献，且文献语种为英文，检
# 索词为“乳房假体”“淋巴瘤…‘原发性T细胞乳腺淋巴瘤…‘乳房假体和ALCL”。结果共纳入18篇
# 文献，包括27例乳房置入假体后发生ALCL的病例。无论是否有乳房假体置入史，与乳房相关的ALCL
# 均可能发生。在27例患者中，21例(78％)CD30间变性淋巴瘤激酶为阴性，表现为无痛的临床病程。
# 报道中使用的乳房假体填充物包括盐水和硅胶；然而，多数报道没有报道假体类型和表面是光面还是毛
# 面。肿瘤分期：I期16例，Ⅱ期及以上7例，未报道4例。没有前瞻性流行病学研究报道乳房假体与
# ALCL之间具有相关性；然而，只有l项以荷兰女性为研究对象的单例病例对照研究报道了乳房置入假
# 体患者发生ALCL的风险会增加，其估算的概率为百万分之一。结论许多研究已报道了乳房假体与
# ALCL之间具有相关关系，但没有因果关系的证据，还需要进一步地通过研究来证实这种相关关系。与
# 乳房相关的ALCL发生率很低(无论是否有乳房假体置入史)，其通常表现为无痛的临床病程，这一发现
# 可能导致世界卫生组织修改淋巴瘤的命名；但是，也有研究报道了其临床表现具有侵袭性。ALCL的发
# 生不限于某种特定类型的假体(临床问题／证据等级：风险，V)。
# 文本到此为止。
# 输出格式需要为以下格式，例如：
# 文本摘要：
# 具体摘要内容
# 示例到此为止。
# 注意：生成的摘要必须按照以上示例的格式进行生成，但是不能引用以上示例的内容！生成的摘要必须来源于用户提供的文本，不可以生成其他无关的内容！只生成摘要，不要生成其他引导、解释的内容，比如“以下为xxx的的概括总结”等！
# """
# first_feasibility_report_prompt = """你现在是一个从事文字编写的专业人员，现在需要攥写一篇可行性研究报告，现在开始写第一章项目概论，这一章分成三节，具体结构如下
#             可行性研究报告
#             第一节 项目基本概况
#             一、项目名称
#             二、项目建设地点
#             三、项目建设内容
#             四、项目建设规模
#             五、项目投资规模及资金筹措
#             第二节 报告主要研究内容及编制依据
#             一、报告研究内容及研究方法
#             二、报告编制依据。
#             第三节 项目主要财务指标
#             参考材料如下：我想写一篇关于人工智能方面的报告，项目名称人工智能的发展现状，建设地点产业园，财务指标为ROI 20%，参考资料到此结束。
#             写作要求：
#             1、一定不要修改上述结构中的内容；
#             2、要注意返回漂亮的格式；
#             3、开头不要出现"根据参考材料"等无意义的内容；
#             4、必须根据参考资料生成500字的研究内容；
#             请你仔细思考，分析以上要求，认真开始写作，不急慢慢来。
# """

# first_feasibility_report_prompt = """你现在是一个从事文字编写的专业人员，现在需要攥写一篇可行性研究报告，现在开始写第一章项目概论，这一章分成三节，具体结构如下
#             可行性研究报告
#             一、目的和意义（按项目申报指南要求填写）
#             1.描述项目研究的必要性（拟解决的问题等）；
#             2.描述项目的总体目标（成果所能达到的水平、应用价值等）。
#             二、项目研究的背景
#             三、项目申请单位具备的研究基础和条件
#             1.项目申请单位在相关研究领域曾开展的工作、曾取得的科研成果、曾获得的荣誉情况；
#             2.项目申请单位在相关研究领域已有的软硬件平台、理论研究基础、实验室条件等情况。
#             四、研究目标及主要研究内容
#             课题（任务）1
#             研究目标：
#             主要研究内容：
#             课题（任务）2
#             研究目标：
#             主要研究内容：
#             课题（任务）3
#             研究目标：
#             主要研究内容：
#             课题（任务）4
#             研究目标：
#             主要研究内容：
#             课题（任务）5
#             研究目标：
#             主要研究内容：
#             五、考核指标
#             六、交付成果
#             七、项目经费预算
#             八、有关证明文件
#             参考材料如下：我想写一篇关于人工智能方面的报告，项目名称人工智能的发展现状，建设地点产业园，财务指标为ROI 20%，参考资料到此结束。
#             写作要求：
#             1、一定不要修改上述结构中的内容；
#             2、要注意返回漂亮的格式；
#             3、开头不要出现"根据参考材料"等无意义的内容；
#             4、必须根据参考资料生成500字的研究内容；
#             请你仔细思考，分析以上要求，认真开始写作，不急慢慢来。
# """

# 获取周报prompt
def get_feasibility_report_prompt(query, knowledge, mode="all", section = ""):
    """
        获取对应模板不通占位符的prompt
        param stage: 组成规则 第一个数字代表模板id对应的序号, 第二个代码该模板的占位符所代表的索引
    """
    if mode == "sec":
        return feasibility_report_prompt.format(section, query, knowledge, section)
    elif mode == "dir":
        return dir_feasibility_report_prompt.format(query, knowledge)
    elif mode == "all":
        return all_feasibility_report_prompt.format(query, knowledge)
    # elif stage == "0_1":
    #     return second_feasibility_report_prompt.format(query)
    # if stage == "0_2":
    #     return third_feasibility_report_prompt.format(query)
    else:
        raise NotImplementedError